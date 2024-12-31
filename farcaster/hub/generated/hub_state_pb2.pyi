from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class HubState(_message.Message):
    __slots__ = ["last_eth_block", "last_fname_proof"]
    LAST_ETH_BLOCK_FIELD_NUMBER: _ClassVar[int]
    LAST_FNAME_PROOF_FIELD_NUMBER: _ClassVar[int]
    last_eth_block: int
    last_fname_proof: int
    def __init__(
        self,
        last_eth_block: _Optional[int] = ...,
        last_fname_proof: _Optional[int] = ...,
    ) -> None: ...
