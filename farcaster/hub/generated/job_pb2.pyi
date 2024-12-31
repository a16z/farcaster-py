from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class RevokeMessagesBySignerJobPayload(_message.Message):
    __slots__ = ["fid", "signer"]
    FID_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    fid: int
    signer: bytes
    def __init__(
        self, fid: _Optional[int] = ..., signer: _Optional[bytes] = ...
    ) -> None: ...

class UpdateNameRegistryEventExpiryJobPayload(_message.Message):
    __slots__ = ["fname"]
    FNAME_FIELD_NUMBER: _ClassVar[int]
    fname: bytes
    def __init__(self, fname: _Optional[bytes] = ...) -> None: ...
