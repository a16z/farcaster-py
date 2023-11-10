from abc import ABC, abstractmethod

from eth_account import Account
from eth_account.messages import encode_structured_data
from nacl.encoding import RawEncoder
from nacl.signing import SigningKey

from farcaster.hub.generated.message_pb2 import SignatureScheme


class Signer(ABC):
    @abstractmethod
    def public_key(self) -> bytes:
        pass

    @abstractmethod
    def private_key(self) -> bytes:
        pass

    @abstractmethod
    def signature_scheme(self) -> SignatureScheme:
        pass

    @abstractmethod
    def sign_hash(self, hash: bytes) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def generate(cls) -> "Signer":
        pass


class EIP712Signer(Signer):
    def __init__(self, account: Account) -> None:
        self.account = account

    def public_key(self) -> bytes:
        return bytes.fromhex(self.account.address[2:])

    def private_key(self) -> bytes:
        return self.account.key

    def signature_scheme(self) -> SignatureScheme:
        return SignatureScheme.SIGNATURE_SCHEME_EIP712

    def sign_hash(self, hash: bytes) -> bytes:
        eip712_schema = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "salt", "type": "bytes32"},
                ],
                "MessageData": [
                    {"name": "hash", "type": "bytes"},
                ],
            },
            "domain": {
                "name": "Farcaster Verify Ethereum Address",
                "version": "2.0.0",
                # fixed salt to minimize collisions, should be the same as
                # packages/core/src/crypto/eip712.ts in @farcaster/hub-monorepo
                "salt": bytes.fromhex(
                    "f2d857f4a3edcb9b78b4d503bfe733db1e3f6cdc2b7971ee739626c97e86a558"
                ),
            },
            "primaryType": "MessageData",
            "message": {
                "hash": hash,
            },
        }

        encoded_message = encode_structured_data(eip712_schema)
        signature = self.account.sign_message(encoded_message)
        return bytes(signature.signature)

    @classmethod
    def generate(cls) -> "EIP712Signer":
        return cls(Account.create())


class Ed25519Signer(Signer):
    def __init__(self, signing_key: SigningKey) -> None:
        self.signing_key = signing_key

    def public_key(self, encoder=RawEncoder) -> bytes:
        return self.signing_key.verify_key.encode(encoder=encoder)

    def private_key(self, encoder=RawEncoder) -> bytes:
        return self.signing_key.encode(encoder=encoder)

    def signature_scheme(self) -> SignatureScheme:
        return SignatureScheme.SIGNATURE_SCHEME_ED25519

    def sign_hash(self, hash: bytes) -> bytes:
        return self.signing_key.sign(hash).signature

    @classmethod
    def generate(cls) -> "Ed25519Signer":
        return cls(SigningKey.generate())
