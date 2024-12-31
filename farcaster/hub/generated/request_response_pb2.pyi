from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

import farcaster.hub.generated.hub_event_pb2 as _hub_event_pb2
import farcaster.hub.generated.message_pb2 as _message_pb2
import farcaster.hub.generated.onchain_event_pb2 as _onchain_event_pb2
import farcaster.hub.generated.username_proof_pb2 as _username_proof_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class StoreType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    STORE_TYPE_NONE: _ClassVar[StoreType]
    STORE_TYPE_CASTS: _ClassVar[StoreType]
    STORE_TYPE_LINKS: _ClassVar[StoreType]
    STORE_TYPE_REACTIONS: _ClassVar[StoreType]
    STORE_TYPE_USER_DATA: _ClassVar[StoreType]
    STORE_TYPE_VERIFICATIONS: _ClassVar[StoreType]

STORE_TYPE_NONE: StoreType
STORE_TYPE_CASTS: StoreType
STORE_TYPE_LINKS: StoreType
STORE_TYPE_REACTIONS: StoreType
STORE_TYPE_USER_DATA: StoreType
STORE_TYPE_VERIFICATIONS: StoreType

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SubscribeRequest(_message.Message):
    __slots__ = ["event_types", "from_id"]
    EVENT_TYPES_FIELD_NUMBER: _ClassVar[int]
    FROM_ID_FIELD_NUMBER: _ClassVar[int]
    event_types: _containers.RepeatedScalarFieldContainer[_hub_event_pb2.HubEventType]
    from_id: int
    def __init__(
        self,
        event_types: _Optional[
            _Iterable[_Union[_hub_event_pb2.HubEventType, str]]
        ] = ...,
        from_id: _Optional[int] = ...,
    ) -> None: ...

class EventRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class HubInfoRequest(_message.Message):
    __slots__ = ["db_stats"]
    DB_STATS_FIELD_NUMBER: _ClassVar[int]
    db_stats: bool
    def __init__(self, db_stats: bool = ...) -> None: ...

class HubInfoResponse(_message.Message):
    __slots__ = ["version", "is_syncing", "nickname", "root_hash", "db_stats"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_SYNCING_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    ROOT_HASH_FIELD_NUMBER: _ClassVar[int]
    DB_STATS_FIELD_NUMBER: _ClassVar[int]
    version: str
    is_syncing: bool
    nickname: str
    root_hash: str
    db_stats: DbStats
    def __init__(
        self,
        version: _Optional[str] = ...,
        is_syncing: bool = ...,
        nickname: _Optional[str] = ...,
        root_hash: _Optional[str] = ...,
        db_stats: _Optional[_Union[DbStats, _Mapping]] = ...,
    ) -> None: ...

class DbStats(_message.Message):
    __slots__ = ["num_messages", "num_fid_events", "num_fname_events"]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NUM_FID_EVENTS_FIELD_NUMBER: _ClassVar[int]
    NUM_FNAME_EVENTS_FIELD_NUMBER: _ClassVar[int]
    num_messages: int
    num_fid_events: int
    num_fname_events: int
    def __init__(
        self,
        num_messages: _Optional[int] = ...,
        num_fid_events: _Optional[int] = ...,
        num_fname_events: _Optional[int] = ...,
    ) -> None: ...

class SyncStatusRequest(_message.Message):
    __slots__ = ["peerId"]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    def __init__(self, peerId: _Optional[str] = ...) -> None: ...

class SyncStatusResponse(_message.Message):
    __slots__ = ["is_syncing", "sync_status", "engine_started"]
    IS_SYNCING_FIELD_NUMBER: _ClassVar[int]
    SYNC_STATUS_FIELD_NUMBER: _ClassVar[int]
    ENGINE_STARTED_FIELD_NUMBER: _ClassVar[int]
    is_syncing: bool
    sync_status: _containers.RepeatedCompositeFieldContainer[SyncStatus]
    engine_started: bool
    def __init__(
        self,
        is_syncing: bool = ...,
        sync_status: _Optional[_Iterable[_Union[SyncStatus, _Mapping]]] = ...,
        engine_started: bool = ...,
    ) -> None: ...

class SyncStatus(_message.Message):
    __slots__ = [
        "peerId",
        "inSync",
        "shouldSync",
        "divergencePrefix",
        "divergenceSecondsAgo",
        "theirMessages",
        "ourMessages",
        "lastBadSync",
    ]
    PEERID_FIELD_NUMBER: _ClassVar[int]
    INSYNC_FIELD_NUMBER: _ClassVar[int]
    SHOULDSYNC_FIELD_NUMBER: _ClassVar[int]
    DIVERGENCEPREFIX_FIELD_NUMBER: _ClassVar[int]
    DIVERGENCESECONDSAGO_FIELD_NUMBER: _ClassVar[int]
    THEIRMESSAGES_FIELD_NUMBER: _ClassVar[int]
    OURMESSAGES_FIELD_NUMBER: _ClassVar[int]
    LASTBADSYNC_FIELD_NUMBER: _ClassVar[int]
    peerId: str
    inSync: str
    shouldSync: bool
    divergencePrefix: str
    divergenceSecondsAgo: int
    theirMessages: int
    ourMessages: int
    lastBadSync: int
    def __init__(
        self,
        peerId: _Optional[str] = ...,
        inSync: _Optional[str] = ...,
        shouldSync: bool = ...,
        divergencePrefix: _Optional[str] = ...,
        divergenceSecondsAgo: _Optional[int] = ...,
        theirMessages: _Optional[int] = ...,
        ourMessages: _Optional[int] = ...,
        lastBadSync: _Optional[int] = ...,
    ) -> None: ...

class TrieNodeMetadataResponse(_message.Message):
    __slots__ = ["prefix", "num_messages", "hash", "children"]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    num_messages: int
    hash: str
    children: _containers.RepeatedCompositeFieldContainer[TrieNodeMetadataResponse]
    def __init__(
        self,
        prefix: _Optional[bytes] = ...,
        num_messages: _Optional[int] = ...,
        hash: _Optional[str] = ...,
        children: _Optional[
            _Iterable[_Union[TrieNodeMetadataResponse, _Mapping]]
        ] = ...,
    ) -> None: ...

class TrieNodeSnapshotResponse(_message.Message):
    __slots__ = ["prefix", "excluded_hashes", "num_messages", "root_hash"]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_HASHES_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    ROOT_HASH_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    excluded_hashes: _containers.RepeatedScalarFieldContainer[str]
    num_messages: int
    root_hash: str
    def __init__(
        self,
        prefix: _Optional[bytes] = ...,
        excluded_hashes: _Optional[_Iterable[str]] = ...,
        num_messages: _Optional[int] = ...,
        root_hash: _Optional[str] = ...,
    ) -> None: ...

class TrieNodePrefix(_message.Message):
    __slots__ = ["prefix"]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    prefix: bytes
    def __init__(self, prefix: _Optional[bytes] = ...) -> None: ...

class SyncIds(_message.Message):
    __slots__ = ["sync_ids"]
    SYNC_IDS_FIELD_NUMBER: _ClassVar[int]
    sync_ids: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, sync_ids: _Optional[_Iterable[bytes]] = ...) -> None: ...

class FidRequest(_message.Message):
    __slots__ = ["fid", "page_size", "page_token", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        fid: _Optional[int] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class FidsRequest(_message.Message):
    __slots__ = ["page_size", "page_token", "reverse"]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class FidsResponse(_message.Message):
    __slots__ = ["fids", "next_page_token"]
    FIDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    fids: _containers.RepeatedScalarFieldContainer[int]
    next_page_token: bytes
    def __init__(
        self,
        fids: _Optional[_Iterable[int]] = ...,
        next_page_token: _Optional[bytes] = ...,
    ) -> None: ...

class MessagesResponse(_message.Message):
    __slots__ = ["messages", "next_page_token"]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    next_page_token: bytes
    def __init__(
        self,
        messages: _Optional[_Iterable[_Union[_message_pb2.Message, _Mapping]]] = ...,
        next_page_token: _Optional[bytes] = ...,
    ) -> None: ...

class CastsByParentRequest(_message.Message):
    __slots__ = ["parent_cast_id", "parent_url", "page_size", "page_token", "reverse"]
    PARENT_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_URL_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    parent_cast_id: _message_pb2.CastId
    parent_url: str
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        parent_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ...,
        parent_url: _Optional[str] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class ReactionRequest(_message.Message):
    __slots__ = ["fid", "reaction_type", "target_cast_id", "target_url"]
    FID_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_URL_FIELD_NUMBER: _ClassVar[int]
    fid: int
    reaction_type: _message_pb2.ReactionType
    target_cast_id: _message_pb2.CastId
    target_url: str
    def __init__(
        self,
        fid: _Optional[int] = ...,
        reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ...,
        target_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ...,
        target_url: _Optional[str] = ...,
    ) -> None: ...

class ReactionsByFidRequest(_message.Message):
    __slots__ = ["fid", "reaction_type", "page_size", "page_token", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    reaction_type: _message_pb2.ReactionType
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        fid: _Optional[int] = ...,
        reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class ReactionsByTargetRequest(_message.Message):
    __slots__ = [
        "target_cast_id",
        "target_url",
        "reaction_type",
        "page_size",
        "page_token",
        "reverse",
    ]
    TARGET_CAST_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_URL_FIELD_NUMBER: _ClassVar[int]
    REACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    target_cast_id: _message_pb2.CastId
    target_url: str
    reaction_type: _message_pb2.ReactionType
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        target_cast_id: _Optional[_Union[_message_pb2.CastId, _Mapping]] = ...,
        target_url: _Optional[str] = ...,
        reaction_type: _Optional[_Union[_message_pb2.ReactionType, str]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class UserDataRequest(_message.Message):
    __slots__ = ["fid", "user_data_type"]
    FID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    user_data_type: _message_pb2.UserDataType
    def __init__(
        self,
        fid: _Optional[int] = ...,
        user_data_type: _Optional[_Union[_message_pb2.UserDataType, str]] = ...,
    ) -> None: ...

class NameRegistryEventRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: bytes
    def __init__(self, name: _Optional[bytes] = ...) -> None: ...

class RentRegistryEventsRequest(_message.Message):
    __slots__ = ["fid"]
    FID_FIELD_NUMBER: _ClassVar[int]
    fid: int
    def __init__(self, fid: _Optional[int] = ...) -> None: ...

class OnChainEventRequest(_message.Message):
    __slots__ = ["fid", "event_type"]
    FID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    event_type: _onchain_event_pb2.OnChainEventType
    def __init__(
        self,
        fid: _Optional[int] = ...,
        event_type: _Optional[_Union[_onchain_event_pb2.OnChainEventType, str]] = ...,
    ) -> None: ...

class OnChainEventResponse(_message.Message):
    __slots__ = ["events"]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_onchain_event_pb2.OnChainEvent]
    def __init__(
        self,
        events: _Optional[
            _Iterable[_Union[_onchain_event_pb2.OnChainEvent, _Mapping]]
        ] = ...,
    ) -> None: ...

class StorageLimitsResponse(_message.Message):
    __slots__ = ["limits"]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    limits: _containers.RepeatedCompositeFieldContainer[StorageLimit]
    def __init__(
        self, limits: _Optional[_Iterable[_Union[StorageLimit, _Mapping]]] = ...
    ) -> None: ...

class StorageLimit(_message.Message):
    __slots__ = ["store_type", "limit"]
    STORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    store_type: StoreType
    limit: int
    def __init__(
        self,
        store_type: _Optional[_Union[StoreType, str]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class UsernameProofRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: bytes
    def __init__(self, name: _Optional[bytes] = ...) -> None: ...

class UsernameProofsResponse(_message.Message):
    __slots__ = ["proofs"]
    PROOFS_FIELD_NUMBER: _ClassVar[int]
    proofs: _containers.RepeatedCompositeFieldContainer[
        _username_proof_pb2.UserNameProof
    ]
    def __init__(
        self,
        proofs: _Optional[
            _Iterable[_Union[_username_proof_pb2.UserNameProof, _Mapping]]
        ] = ...,
    ) -> None: ...

class VerificationRequest(_message.Message):
    __slots__ = ["fid", "address"]
    FID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    fid: int
    address: bytes
    def __init__(
        self, fid: _Optional[int] = ..., address: _Optional[bytes] = ...
    ) -> None: ...

class SignerRequest(_message.Message):
    __slots__ = ["fid", "signer"]
    FID_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    fid: int
    signer: bytes
    def __init__(
        self, fid: _Optional[int] = ..., signer: _Optional[bytes] = ...
    ) -> None: ...

class LinkRequest(_message.Message):
    __slots__ = ["fid", "link_type", "target_fid"]
    FID_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FID_FIELD_NUMBER: _ClassVar[int]
    fid: int
    link_type: str
    target_fid: int
    def __init__(
        self,
        fid: _Optional[int] = ...,
        link_type: _Optional[str] = ...,
        target_fid: _Optional[int] = ...,
    ) -> None: ...

class LinksByFidRequest(_message.Message):
    __slots__ = ["fid", "link_type", "page_size", "page_token", "reverse"]
    FID_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    fid: int
    link_type: str
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        fid: _Optional[int] = ...,
        link_type: _Optional[str] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class LinksByTargetRequest(_message.Message):
    __slots__ = ["target_fid", "link_type", "page_size", "page_token", "reverse"]
    TARGET_FID_FIELD_NUMBER: _ClassVar[int]
    LINK_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    target_fid: int
    link_type: str
    page_size: int
    page_token: bytes
    reverse: bool
    def __init__(
        self,
        target_fid: _Optional[int] = ...,
        link_type: _Optional[str] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[bytes] = ...,
        reverse: bool = ...,
    ) -> None: ...

class IdRegistryEventRequest(_message.Message):
    __slots__ = ["fid"]
    FID_FIELD_NUMBER: _ClassVar[int]
    fid: int
    def __init__(self, fid: _Optional[int] = ...) -> None: ...

class IdRegistryEventByAddressRequest(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    def __init__(self, address: _Optional[bytes] = ...) -> None: ...
