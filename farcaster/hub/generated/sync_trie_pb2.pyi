from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class DbTrieNode(_message.Message):
    __slots__ = ["key", "childChars", "items", "hash"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    CHILDCHARS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    key: bytes
    childChars: _containers.RepeatedScalarFieldContainer[int]
    items: int
    hash: bytes
    def __init__(
        self,
        key: _Optional[bytes] = ...,
        childChars: _Optional[_Iterable[int]] = ...,
        items: _Optional[int] = ...,
        hash: _Optional[bytes] = ...,
    ) -> None: ...
