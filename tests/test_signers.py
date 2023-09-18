import pytest

from farcaster.hub.generated.message_pb2 import SignatureScheme
from farcaster.hub.signers import Ed25519Signer, EIP712Signer, Signer


# Test cases
@pytest.mark.parametrize(
    "signer_class,expected_scheme",
    [
        (EIP712Signer, SignatureScheme.SIGNATURE_SCHEME_EIP712),
        (Ed25519Signer, SignatureScheme.SIGNATURE_SCHEME_ED25519),
    ],
)
def test_signer(signer_class: Signer, expected_scheme: SignatureScheme):
    signer = signer_class.generate()

    assert signer.signature_scheme() == expected_scheme

    assert isinstance(signer.private_key(), bytes)
    assert isinstance(signer.public_key(), bytes)

    hash_data = b"test message"
    signature = signer.sign_hash(hash_data)
    assert isinstance(signature, bytes)
    assert len(signature) > 0
