from typing import List, Optional

import json
from pathlib import Path

import requests
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

from farcaster.types import Cast, HostDirectory, User


class FarcasterClient:
    # Farcaster registry Rinkeby contract addr
    __REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
    # Farcaster registry ABI
    DEFAULT_DIRECTORY_URL = "https://guardian.farcaster.xyz/origin/directory/"
    DEFAULT_HOST_URL = "https://guardian.farcaster.xyz/"

    def __init__(
        self,
        rinkeby_network_conn_str: str,
        registry_contract_address: Optional[str] = None,
        signature_account: Optional[LocalAccount] = None,
    ):
        self.signature_account = signature_account
        web3_provider = Web3.HTTPProvider(rinkeby_network_conn_str)
        self.w3 = Web3(web3_provider)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        parent_path = Path(__file__).parent.resolve()
        registry_abi = parent_path.joinpath(Path("registry_abi.json"))
        with open(registry_abi) as f:
            self.ABI = json.load(f)
        if registry_contract_address:
            self.registry_contract_address = registry_contract_address
        else:
            self.registry_contract_address = self.__REGISTRY_CONTRACT_ADDRESS
        self.registry = self.w3.eth.contract(
            address=self.registry_contract_address, abi=self.ABI
        )

    def get_profile(self, username: str) -> HostDirectory:
        host_addr = self.get_host_addr(username)
        return HostDirectory.parse_obj(requests.get(host_addr).json())

    def verify_cast(self, cast: Cast) -> bool:
        calculated_hash = Web3.toHex(
            Web3.keccak(
                Web3.toBytes(
                    text=cast.body.json(
                        by_alias=True, exclude_none=True, separators=(",", ":")
                    )
                )
            )
        )
        expected_hash = cast.merkle_root

        if calculated_hash != expected_hash:
            print(f"{calculated_hash} does not equal {expected_hash}!")
            return False

        encoded = encode_defunct(text=cast.merkle_root)
        recovered_address = self.w3.eth.account.recover_message(
            encoded, signature=cast.signature
        )
        expected_address = cast.body.address

        if recovered_address != expected_address:
            print(f"{recovered_address} does not equal {expected_address}!")
            return False

        encoded_username = self.get_username(expected_address)

        if encoded_username != cast.body.username:
            print(f"{encoded_username} does not equal {cast.body.username}!")
            return False

        return True

    def get_casts(self, username: str) -> List[Cast]:
        caster = self.get_profile(username)
        response = requests.get(caster.body.address_activity_url).json()
        return [Cast.parse_obj(cast) for cast in response]

    def get_host_addr(self, username: str) -> str:
        encoded_username = Web3.toBytes(text=username)
        host_address: str = self.registry.caller().getDirectoryUrl(encoded_username)
        return host_address

    def get_username(self, expected_address: str) -> str:
        encoded_address = self.registry.caller().addressToUsername(
            Web3.toChecksumAddress(expected_address)
        )
        return Web3.toText(encoded_address).rstrip("\x00")

    def register(self, username: str, url: str = DEFAULT_DIRECTORY_URL) -> str:
        assert self.signature_account
        directory_url = url + Web3.toChecksumAddress(self.signature_account.address)
        encoded_username = Web3.toBytes(text=username)
        nonce = self.w3.eth.get_transaction_count(
            self.signature_account.address, "pending"
        )
        transaction = self.registry.functions.register(
            encoded_username, directory_url
        ).build_transaction({"nonce": nonce})
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, self.signature_account.key
        )
        response = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return response.hex()

    def transfer(self, to: str) -> str:
        assert self.signature_account
        nonce = self.w3.eth.get_transaction_count(
            self.signature_account.address, "pending"
        )
        transaction = self.registry.functions.transfer(
            Web3.toChecksumAddress(to)
        ).build_transaction({"nonce": nonce})
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, self.signature_account.key
        )
        response = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return response.hex()

    # User Registry

    def lookup_by_username(self, username: str) -> Optional[User]:
        response = requests.get(self.DEFAULT_HOST_URL + "admin/usernames/" + username)
        if response.status_code == 404:
            return None
        return User.parse_obj(response.json())

    def get_all_users(self) -> Optional[List[User]]:
        response = requests.get(self.DEFAULT_HOST_URL + "admin/usernames")
        if response.status_code == 404:
            return None
        return [User.parse_obj(user) for user in response.json()]

    def get_all_usernames(self) -> Optional[List[str]]:
        users = self.get_all_users()
        if users:
            return [user.username for user in users]
        return None

    def lookup_by_address(self, address: str) -> Optional[User]:
        users = self.get_all_users()
        if users:
            for user in users:
                if user.address == address:
                    return user
        return None
