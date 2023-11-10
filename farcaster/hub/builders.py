from blake3 import blake3

from farcaster.hub.generated.message_pb2 import (
    CastAddBody,
    HashScheme,
    Message,
    MessageData,
    MessageType,
    SignerAddBody,
)
from farcaster.hub.signers import Ed25519Signer, Signer


def _make_message(data: MessageData, signer: Signer) -> Message:
    hash = blake3(data.SerializeToString()).digest(length=20)
    return Message(
        data=data,
        hash=hash,
        hash_scheme=HashScheme.HASH_SCHEME_BLAKE3,
        signature=signer.sign_hash(hash),
        signature_scheme=signer.signature_scheme(),
        signer=signer.public_key(),
    )


def make_signer_add(
    data: MessageData, signer: Signer, signer_add: Ed25519Signer
) -> Message:
    # Create a new MessageData object and copy the provided data
    message_data = MessageData()
    message_data.CopyFrom(data)
    message_data.type = MessageType.MESSAGE_TYPE_SIGNER_ADD
    message_data.signer_add_body.CopyFrom(SignerAddBody(signer=signer_add.public_key()))
    return _make_message(
        message_data,
        signer,
    )


def make_cast_add(data: MessageData, signer: Signer, cast_add: CastAddBody) -> Message:
    # Create a new MessageData object and copy the provided data
    message_data = MessageData()
    message_data.CopyFrom(data)
    message_data.type = MessageType.MESSAGE_TYPE_CAST_ADD
    message_data.cast_add_body.CopyFrom(cast_add)
    return _make_message(
        message_data,
        signer,
    )
