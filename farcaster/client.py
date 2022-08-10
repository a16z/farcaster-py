from typing import List, Optional, Union

import json
from datetime import datetime
from pathlib import Path

import requests
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import geth_poa_middleware

from farcaster import types


class FarcasterClient:
    # Farcaster registry Rinkeby contract addr
    __REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
    # Farcaster registry ABI
    DEFAULT_DIRECTORY_URL = "https://guardian.farcaster.xyz/origin/directory/"
    DEFAULT_HOST_URL = "https://guardian.farcaster.xyz/"
    CAST_CHARACTER_LIMIT = 280

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

    def get_profile(self, username: str) -> types.HostDirectory:
        host_addr = self.get_host_addr(username)
        print(host_addr)
        return types.HostDirectory.parse_obj(requests.get(host_addr).json())

    def verify_cast(self, cast: types.AddressActivity) -> bool:
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

    def get_casts(self, username: str) -> List[types.AddressActivity]:
        print(username)
        caster = self.get_profile(username)
        response = requests.get(caster.body.address_activity_url).json()
        return [types.AddressActivity.parse_obj(cast) for cast in response]

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
        print(self.signature_account.address)
        directory_url = url + Web3.toChecksumAddress(self.signature_account.address)
        encoded_username = Web3.toBytes(text=username)
        nonce = self.w3.eth.get_transaction_count(
            self.signature_account.address, "pending"
        )
        print(nonce)
        transaction = self.registry.functions.register(
            encoded_username, directory_url
        ).build_transaction({"nonce": nonce})
        signed_tx = self.w3.eth.account.sign_transaction(
            transaction, self.signature_account.key
        )
        response = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(response)

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

    def lookup_by_username(self, username: str) -> Optional[types.User]:
        response = requests.get(self.DEFAULT_HOST_URL + "admin/usernames/" + username)
        if response.status_code == 404:
            return None
        return types.User.parse_obj(response.json())

    def get_all_users(self) -> Optional[List[types.User]]:
        response = requests.get(self.DEFAULT_HOST_URL + "admin/usernames")
        if response.status_code == 404:
            return None
        return [types.User.parse_obj(user) for user in response.json()]

    def get_all_usernames(self) -> Optional[List[str]]:
        users = self.get_all_users()
        if users:
            return [user.username for user in users]
        return None

    def lookup_by_address(self, address: str) -> Optional[types.User]:
        users = self.get_all_users()
        if users:
            for user in users:
                if user.address == address:
                    return user
        return None

    def get_latest_activity_for_user(
        self, username: str
    ) -> Optional[types.AddressActivity]:
        activity = self.get_casts(username)
        if len(activity) > 0:
            return activity[0]
        return None

    def prepare_cast(
        self,
        username: str,
        text: str,
        reply_to: Optional[Union[types.AddressActivity, str]],
    ) -> types.AddressActivityBody:
        assert self.signature_account
        if len(text) >= self.CAST_CHARACTER_LIMIT:
            raise ValueError(
                f"Cast length must be less than {self.CAST_CHARACTER_LIMIT}"
            )
        reply_parent_merkle_root = None
        if reply_to:
            if type(reply_to) == str:
                reply_parent_merkle_root = reply_to
            else:
                reply_parent_merkle_root = reply_to.merkle_root
        user_activity = self.get_latest_activity_for_user(username)

        if not user_activity:
            user = self.lookup_by_address(self.signature_account.address)
            if not user:
                raise ValueError("no username registered for address")
            address = user.address
            prev_merkle_root = Web3.keccak(Web3.toBytes(text=""))
            sequence = 0
        else:
            address = user_activity.body.address
            prev_merkle_root = user_activity.merkle_root
            sequence = user_activity.body.sequence + 1

        data = types.CastData(
            text=text, reply_parent_merkle_root=reply_parent_merkle_root
        )

        return types.AddressActivityBody(
            type=types.AddressActivityBodyType.TEXT_SHORT,
            published_at=int(datetime.now().timestamp()),
            sequence=sequence,
            username=username,
            address=address,
            data=data,
            prev_merkle_root=prev_merkle_root,
        )

    def sign_cast(self, unsigned_cast: types.AddressActivityBody) -> types.SignedCast:
        assert self.signature_account
        serialized_cast = unsigned_cast.json(
            by_alias=True, exclude_none=True, separators=(",", ":")
        )
        merkle_root = Web3.toHex(Web3.keccak(Web3.toBytes(text=serialized_cast)))
        encoded = encode_defunct(text=merkle_root)

        signature = self.signature_account.sign_message(encoded)
        print(signature)
        signed_cast = types.SignedCast(
            body=unsigned_cast, merkle_root=merkle_root, signature=signature
        )
        return signed_cast

    def publish_cast(
        self, text: str, reply_to: Optional[Union[types.AddressActivity, str]] = None
    ) -> types.SignedCast:
        assert self.signature_account
        user = self.lookup_by_address(self.signature_account.address)
        if not user:
            raise ValueError("no username registered for address")
        unsigned_cast = self.prepare_cast(user.username, text, reply_to)

        signed_cast = self.sign_cast(unsigned_cast)
        self.post_cast_to_registry(signed_cast)
        return signed_cast

    def post_cast_to_registry(self, signed_cast: types.SignedCast) -> None:
        response = requests.get(
            self.DEFAULT_HOST_URL + "indexer/activity", signed_cast.json(by_alias=True)
        )
        if response.status_code == 404:
            print("404")
            return None
        print(response.json())
        return None
