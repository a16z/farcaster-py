from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class UserNameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    USERNAME_TYPE_NONE: _ClassVar[UserNameType]
    USERNAME_TYPE_FNAME: _ClassVar[UserNameType]
    USERNAME_TYPE_ENS_L1: _ClassVar[UserNameType]

USERNAME_TYPE_NONE: UserNameType
USERNAME_TYPE_FNAME: UserNameType
USERNAME_TYPE_ENS_L1: UserNameType

class UserNameProof(_message.Message):
    __slots__ = ["timestamp", "name", "owner", "signature", "fid", "type"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    name: bytes
    owner: bytes
    signature: bytes
    fid: int
    type: UserNameType
    def __init__(
        self,
        timestamp: _Optional[int] = ...,
        name: _Optional[bytes] = ...,
        owner: _Optional[bytes] = ...,
        signature: _Optional[bytes] = ...,
        fid: _Optional[int] = ...,
        type: _Optional[_Union[UserNameType, str]] = ...,
    ) -> None: ...
