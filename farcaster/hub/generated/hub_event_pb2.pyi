from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

import farcaster.hub.generated.id_registry_event_pb2 as _id_registry_event_pb2
import farcaster.hub.generated.message_pb2 as _message_pb2
import farcaster.hub.generated.name_registry_event_pb2 as _name_registry_event_pb2
import farcaster.hub.generated.onchain_event_pb2 as _onchain_event_pb2
import farcaster.hub.generated.username_proof_pb2 as _username_proof_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class HubEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    HUB_EVENT_TYPE_NONE: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_MERGE_MESSAGE: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_PRUNE_MESSAGE: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_REVOKE_MESSAGE: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_MERGE_ID_REGISTRY_EVENT: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_MERGE_NAME_REGISTRY_EVENT: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_MERGE_USERNAME_PROOF: _ClassVar[HubEventType]
    HUB_EVENT_TYPE_MERGE_ON_CHAIN_EVENT: _ClassVar[HubEventType]

HUB_EVENT_TYPE_NONE: HubEventType
HUB_EVENT_TYPE_MERGE_MESSAGE: HubEventType
HUB_EVENT_TYPE_PRUNE_MESSAGE: HubEventType
HUB_EVENT_TYPE_REVOKE_MESSAGE: HubEventType
HUB_EVENT_TYPE_MERGE_ID_REGISTRY_EVENT: HubEventType
HUB_EVENT_TYPE_MERGE_NAME_REGISTRY_EVENT: HubEventType
HUB_EVENT_TYPE_MERGE_USERNAME_PROOF: HubEventType
HUB_EVENT_TYPE_MERGE_ON_CHAIN_EVENT: HubEventType

class MergeMessageBody(_message.Message):
    __slots__ = ["message", "deleted_messages"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DELETED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    deleted_messages: _containers.RepeatedCompositeFieldContainer[_message_pb2.Message]
    def __init__(
        self,
        message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...,
        deleted_messages: _Optional[
            _Iterable[_Union[_message_pb2.Message, _Mapping]]
        ] = ...,
    ) -> None: ...

class PruneMessageBody(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    def __init__(
        self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...
    ) -> None: ...

class RevokeMessageBody(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _message_pb2.Message
    def __init__(
        self, message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...
    ) -> None: ...

class MergeIdRegistryEventBody(_message.Message):
    __slots__ = ["id_registry_event"]
    ID_REGISTRY_EVENT_FIELD_NUMBER: _ClassVar[int]
    id_registry_event: _id_registry_event_pb2.IdRegistryEvent
    def __init__(
        self,
        id_registry_event: _Optional[
            _Union[_id_registry_event_pb2.IdRegistryEvent, _Mapping]
        ] = ...,
    ) -> None: ...

class MergeNameRegistryEventBody(_message.Message):
    __slots__ = ["name_registry_event"]
    NAME_REGISTRY_EVENT_FIELD_NUMBER: _ClassVar[int]
    name_registry_event: _name_registry_event_pb2.NameRegistryEvent
    def __init__(
        self,
        name_registry_event: _Optional[
            _Union[_name_registry_event_pb2.NameRegistryEvent, _Mapping]
        ] = ...,
    ) -> None: ...

class MergeOnChainEventBody(_message.Message):
    __slots__ = ["on_chain_event"]
    ON_CHAIN_EVENT_FIELD_NUMBER: _ClassVar[int]
    on_chain_event: _onchain_event_pb2.OnChainEvent
    def __init__(
        self,
        on_chain_event: _Optional[
            _Union[_onchain_event_pb2.OnChainEvent, _Mapping]
        ] = ...,
    ) -> None: ...

class MergeUserNameProofBody(_message.Message):
    __slots__ = [
        "username_proof",
        "deleted_username_proof",
        "username_proof_message",
        "deleted_username_proof_message",
    ]
    USERNAME_PROOF_FIELD_NUMBER: _ClassVar[int]
    DELETED_USERNAME_PROOF_FIELD_NUMBER: _ClassVar[int]
    USERNAME_PROOF_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DELETED_USERNAME_PROOF_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    username_proof: _username_proof_pb2.UserNameProof
    deleted_username_proof: _username_proof_pb2.UserNameProof
    username_proof_message: _message_pb2.Message
    deleted_username_proof_message: _message_pb2.Message
    def __init__(
        self,
        username_proof: _Optional[
            _Union[_username_proof_pb2.UserNameProof, _Mapping]
        ] = ...,
        deleted_username_proof: _Optional[
            _Union[_username_proof_pb2.UserNameProof, _Mapping]
        ] = ...,
        username_proof_message: _Optional[_Union[_message_pb2.Message, _Mapping]] = ...,
        deleted_username_proof_message: _Optional[
            _Union[_message_pb2.Message, _Mapping]
        ] = ...,
    ) -> None: ...

class HubEvent(_message.Message):
    __slots__ = [
        "type",
        "id",
        "merge_message_body",
        "prune_message_body",
        "revoke_message_body",
        "merge_id_registry_event_body",
        "merge_name_registry_event_body",
        "merge_username_proof_body",
        "merge_on_chain_event_body",
    ]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MERGE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    PRUNE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    REVOKE_MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_ID_REGISTRY_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_NAME_REGISTRY_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_USERNAME_PROOF_BODY_FIELD_NUMBER: _ClassVar[int]
    MERGE_ON_CHAIN_EVENT_BODY_FIELD_NUMBER: _ClassVar[int]
    type: HubEventType
    id: int
    merge_message_body: MergeMessageBody
    prune_message_body: PruneMessageBody
    revoke_message_body: RevokeMessageBody
    merge_id_registry_event_body: MergeIdRegistryEventBody
    merge_name_registry_event_body: MergeNameRegistryEventBody
    merge_username_proof_body: MergeUserNameProofBody
    merge_on_chain_event_body: MergeOnChainEventBody
    def __init__(
        self,
        type: _Optional[_Union[HubEventType, str]] = ...,
        id: _Optional[int] = ...,
        merge_message_body: _Optional[_Union[MergeMessageBody, _Mapping]] = ...,
        prune_message_body: _Optional[_Union[PruneMessageBody, _Mapping]] = ...,
        revoke_message_body: _Optional[_Union[RevokeMessageBody, _Mapping]] = ...,
        merge_id_registry_event_body: _Optional[
            _Union[MergeIdRegistryEventBody, _Mapping]
        ] = ...,
        merge_name_registry_event_body: _Optional[
            _Union[MergeNameRegistryEventBody, _Mapping]
        ] = ...,
        merge_username_proof_body: _Optional[
            _Union[MergeUserNameProofBody, _Mapping]
        ] = ...,
        merge_on_chain_event_body: _Optional[
            _Union[MergeOnChainEventBody, _Mapping]
        ] = ...,
    ) -> None: ...
