from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class IdRegistryEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ID_REGISTRY_EVENT_TYPE_NONE: _ClassVar[IdRegistryEventType]
    ID_REGISTRY_EVENT_TYPE_REGISTER: _ClassVar[IdRegistryEventType]
    ID_REGISTRY_EVENT_TYPE_TRANSFER: _ClassVar[IdRegistryEventType]

ID_REGISTRY_EVENT_TYPE_NONE: IdRegistryEventType
ID_REGISTRY_EVENT_TYPE_REGISTER: IdRegistryEventType
ID_REGISTRY_EVENT_TYPE_TRANSFER: IdRegistryEventType

class IdRegistryEvent(_message.Message):
    __slots__ = [
        "block_number",
        "block_hash",
        "transaction_hash",
        "log_index",
        "fid",
        "to",
        "type",
    ]
    BLOCK_NUMBER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_HASH_FIELD_NUMBER: _ClassVar[int]
    LOG_INDEX_FIELD_NUMBER: _ClassVar[int]
    FID_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    block_number: int
    block_hash: bytes
    transaction_hash: bytes
    log_index: int
    fid: int
    to: bytes
    type: IdRegistryEventType
    def __init__(
        self,
        block_number: _Optional[int] = ...,
        block_hash: _Optional[bytes] = ...,
        transaction_hash: _Optional[bytes] = ...,
        log_index: _Optional[int] = ...,
        fid: _Optional[int] = ...,
        to: _Optional[bytes] = ...,
        type: _Optional[_Union[IdRegistryEventType, str]] = ...,
        **kwargs,
    ) -> None: ...
