from typing import List, Optional

import requests
from eth_account.messages import encode_defunct
from web3 import Web3

from farcaster.types import Cast, HostDirectory


class FarcasterClient:
    # Farcaster registry Rinkeby contract addr
    __REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
    # Farcaster registry ABI
    __ABI = '[{"name":"getDirectoryUrl","inputs":[{"internalType":"bytes32","name":"username","type":"bytes32"}],"outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"addressToUsername","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

    def __init__(
        self,
        rinkeby_network_conn_str: str,
        registry_contract_address: Optional[str] = None,
    ):
        web3_provider = Web3.HTTPProvider(rinkeby_network_conn_str)
        self.w3 = Web3(web3_provider)
        if registry_contract_address:
            self.registry_contract_address = registry_contract_address
        else:
            self.registry_contract_address = self.__REGISTRY_CONTRACT_ADDRESS
        self.registry = self.w3.eth.contract(
            address=self.registry_contract_address, abi=self.__ABI
        ).caller()

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
        return self.registry.getDirectoryUrl(encoded_username)

    def get_username(self, expected_address: str) -> str:
        encoded_address = self.registry.addressToUsername(
            Web3.toChecksumAddress(expected_address)
        )
        return Web3.toText(encoded_address).rstrip("\x00")
