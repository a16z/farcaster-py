from __future__ import annotations

from typing import Any, Dict, List, Optional, Type, TypeAlias, Union

from fastapi_camelcase import CamelModel
from pydantic import AnyUrl
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, NoneStr, PositiveInt, conint, constr


class BaseModel(PydanticBaseModel):
    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        if hasattr(kwargs, "exclude_none"):
            _ignored = kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)


class ApiError(BaseModel):
    message: str


class ApiErrorResponse(BaseModel):
    errors: list[ApiError]


class ApiKeyStoreKey(BaseModel):
    key_id: str = Field(..., alias="keyId")
    type: str
    base64_public_key: str = Field(..., alias="base64PublicKey")
    base64_signature: str = Field(..., alias="base64Signature")
    timestamp: PositiveInt
    fid: PositiveInt | None = None
    device_id: NoneStr = Field(None, alias="deviceId")
    device_name: NoneStr = Field(None, alias="deviceName")


class ApiToken(BaseModel):
    secret: str
    expires_at: PositiveInt = Field(..., alias="expiresAt")


class ApiOpenGraphMetadata(BaseModel):
    url: AnyUrl
    title: NoneStr = None
    description: NoneStr = None
    domain: NoneStr = None
    image: str | None = None
    logo: AnyUrl | None = None
    use_large_image: bool | None = Field(None, alias="useLargeImage")
    stripped_cast_text: NoneStr = Field(None, alias="strippedCastText")


class ApiCastAttachments(BaseModel):
    open_graph: list[ApiOpenGraphMetadata] | None = Field(None, alias="openGraph")


class ApiOpenSeaNft(BaseModel):
    asset_contract_address: str
    token_id: str
    account_address: str


class ApiPfp(BaseModel):
    url: AnyUrl
    verified: bool


class Bio(BaseModel):
    text: str
    mentions: list[str]


class ApiProfile(BaseModel):
    bio: Bio


class ViewerContext(BaseModel):
    following: bool | None = None
    followed_by: bool | None = Field(None, alias="followedBy")
    can_send_direct_casts: bool | None = Field(None, alias="canSendDirectCasts")


class ApiUser(BaseModel):
    fid: PositiveInt
    username: str | None = None
    display_name: str | None = Field(None, alias="displayName")
    registered_at: PositiveInt | None = Field(None, alias="registeredAt")
    pfp: ApiPfp | None = None
    profile: ApiProfile
    follower_count: int = Field(..., alias="followerCount")
    following_count: int = Field(..., alias="followingCount")
    referrer_username: str | None = Field(None, alias="referrerUsername")
    viewer_context: ViewerContext | None = Field(None, alias="viewerContext")


class ApiUserPreferences(BaseModel):
    send_email_on_mention: bool | None = Field(None, alias="sendEmailOnMention")
    send_email_on_reply: bool | None = Field(None, alias="sendEmailOnReply")
    send_email_on_reaction: bool | None = Field(None, alias="sendEmailOnReaction")
    send_email_on_follow: bool | None = Field(None, alias="sendEmailOnFollow")
    send_weekly_update_emails: bool | None = Field(None, alias="sendWeeklyUpdateEmails")
    send_product_update_emails: bool | None = Field(
        None, alias="sendProductUpdateEmails"
    )


class ApiAssetCollection(BaseModel):
    id: str
    name: str
    description: NoneStr = None
    item_count: int = Field(..., alias="itemCount")
    owner_count: int = Field(..., alias="ownerCount")
    farcaster_owner_count: int = Field(..., alias="farcasterOwnerCount")
    image_url: str = Field(..., alias="imageUrl")
    floor_price: NoneStr = Field(None, alias="floorPrice")
    volume_traded: str = Field(..., alias="volumeTraded")
    external_url: NoneStr = Field(None, alias="externalUrl")
    open_sea_url: str = Field(..., alias="openSeaUrl")
    twitter_username: NoneStr = Field(None, alias="twitterUsername")
    schema_name: NoneStr = Field(None, alias="schemaName")


class LastSale(BaseModel):
    price: str
    date: str


class Mint(BaseModel):
    date: str
    transaction_hash: str = Field(..., alias="transactionHash")


class ViewerContext1(BaseModel):
    liked: bool | None = None


class ApiAsset(BaseModel):
    id: str
    name: str
    contract_address: str = Field(..., alias="contractAddress")
    token_id: str = Field(..., alias="tokenId")
    image_url: str = Field(..., alias="imageUrl")
    external_url: NoneStr = Field(None, alias="externalUrl")
    open_sea_url: str = Field(..., alias="openSeaUrl")
    like_count: int = Field(..., alias="likeCount")
    uri: str
    collection: ApiAssetCollection
    owner: ApiUser | None = None
    last_sale: LastSale | None = Field(None, alias="lastSale")
    mint: Mint | None = None
    viewer_context: ViewerContext1 | None = Field(None, alias="viewerContext")


class ApiAssetGroup(BaseModel):
    collection: ApiAssetCollection
    assets: list[ApiAsset]


class ApiAssetEvent(BaseModel):
    id: str
    timestamp: PositiveInt
    type: str
    verb: str
    asset: ApiAsset
    user: ApiUser


class ApiAssetEventFeedItem(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    events: list[ApiAssetEvent]


class ApiVerification(BaseModel):
    fid: PositiveInt
    address: str
    timestamp: PositiveInt


class ApiCastReaction(BaseModel):
    type: str
    hash: str
    reactor: ApiUser
    timestamp: PositiveInt
    cast_hash: str = Field(..., alias="castHash", regex=r"^0[xX][0-9a-fA-F]{64}$")


class ApiNewCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent = Field(..., alias="firstEvent")


class ApiTopCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent = Field(..., alias="firstEvent")


class ApiTrendingCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent = Field(..., alias="firstEvent")
    recent_unique_users_count: int = Field(..., alias="recentUniqueUsersCount")


class ApiRecaster(BaseModel):
    fid: PositiveInt
    username: str | None = None
    display_name: str | None = Field(None, alias="displayName")
    recast_hash: str = Field(..., alias="recastHash", regex=r"^0[xX][0-9a-fA-F]{64}$")


class Ancestors(BaseModel):
    count: int


class Replies(BaseModel):
    count: int


class Reactions(BaseModel):
    count: int


class Recasts(BaseModel):
    count: int
    recasters: list[ApiRecaster] | None = None


class Watches(BaseModel):
    count: int


class ViewerContext2(BaseModel):
    reacted: bool | None = None
    recast: bool | None = None
    watched: bool | None = None


class ApiCast(BaseModel):
    hash: str
    thread_hash: NoneStr = Field(None, alias="threadHash")
    parent_hash: NoneStr = Field(None, alias="parentHash")
    author: ApiUser
    text: str
    timestamp: PositiveInt
    mentions: list[ApiUser] | None = None
    attachments: ApiCastAttachments | None = None
    ancestors: Ancestors | None = None
    replies: Replies
    reactions: Reactions
    recasts: Recasts
    watches: Watches
    deleted: bool | None = None
    recast: bool | None = None
    viewer_context: ViewerContext2 | None = Field(None, alias="viewerContext")


class ViewerContext3(BaseModel):
    sender: bool


class ApiDirectCast(BaseModel):
    sender: ApiUser
    text: str
    timestamp: PositiveInt
    viewer_context: ViewerContext3 | None = Field(None, alias="viewerContext")


class ApiDirectCastConversation(BaseModel):
    conversation_id: str = Field(..., alias="conversationId")
    participants: list[ApiUser]
    last_direct_cast: ApiDirectCast = Field(..., alias="lastDirectCast")
    timestamp: PositiveInt


class ApiUnseenConversation(BaseModel):
    conversation_id: str = Field(..., alias="conversationId")
    participant_fids: list[int] = Field(..., alias="participantFids")
    last_direct_cast_timestamp: PositiveInt = Field(
        ..., alias="lastDirectCastTimestamp"
    )


class ReactionContent(BaseModel):
    cast: ApiCast
    reaction: ApiCastReaction


class ApiNotificationCastReaction(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: ReactionContent


class CastContent(BaseModel):
    cast: ApiCast


class ApiNotificationCastMention(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: CastContent


class ApiNotificationCastReply(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: CastContent


class ApiNotificationFollow(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser


class RecastContent(BaseModel):
    recast: ApiCast
    recasted_cast: ApiCast = Field(..., alias="recastedCast")


class ApiNotificationRecast(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: RecastContent


class ReplyContent(BaseModel):
    cast: ApiCast
    reply: ApiCast


class ApiNotificationWatchedCastReply(BaseModel):
    type: str
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: ReplyContent


class ApiNotification(BaseModel):
    __root__: (
        ApiNotificationCastReaction
        | ApiNotificationCastMention
        | ApiNotificationCastReply
        | ApiNotificationFollow
        | ApiNotificationRecast
        | ApiNotificationWatchedCastReply
    ) = Field(..., title="ApiNotification")


class ApiCastReactionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationCastReaction] = Field(..., alias="previewItems")


class ApiCastMentionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationCastMention] = Field(..., alias="previewItems")


class ApiCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationCastReply] = Field(..., alias="previewItems")


class ApiFollowNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationFollow] = Field(..., alias="previewItems")


class ApiRecastNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationRecast] = Field(..., alias="previewItems")


class ApiWatchedCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: list[ApiNotificationWatchedCastReply] = Field(
        ..., alias="previewItems"
    )


class ApiNotificationGroup(BaseModel):
    __root__: (
        ApiCastReactionNotificationGroup
        | ApiCastMentionNotificationGroup
        | ApiCastReplyNotificationGroup
        | ApiFollowNotificationGroup
        | ApiRecastNotificationGroup
        | ApiWatchedCastReplyNotificationGroup
    ) = Field(..., title="ApiNotificationGroup")


class ApiCastFeedItem(BaseModel):
    id: str
    timestamp: PositiveInt
    cast: ApiCast
    replies: list[ApiCast] | None = None
    other_participants: list[ApiUser] = Field(..., alias="otherParticipants")


class ViewCastPushNotification(BaseModel):
    id: str
    type: str
    merkle_root: str = Field(..., alias="merkleRoot")
    thread_merkle_root: str = Field(..., alias="threadMerkleRoot")
    cast_fid: float = Field(..., alias="castFid")
    cast_hash: str = Field(..., alias="castHash")


class UnreadDirectCastPushNotification(BaseModel):
    id: str
    type: str


class PushNotificationPayload(BaseModel):
    __root__: ViewCastPushNotification | UnreadDirectCastPushNotification = Field(
        ..., title="PushNotificationPayload"
    )


class Result(BaseModel):
    status: str


class HealthcheckGetResponse(BaseModel):
    result: Result


class Next(BaseModel):
    cursor: NoneStr = None


class AssetEventsGetResponse(BaseModel):
    result: EventsResult
    next: Next | None = None


class AssetResult(BaseModel):
    asset: ApiAsset


class AssetGetResponse(BaseModel):
    result: AssetResult


class Params(CamelModel):
    timestamp: PositiveInt
    expires_at: PositiveInt | None = Field(None, alias="expiresAt")


class AuthPutRequest(BaseModel):
    method: str = "generateToken"
    params: Params


class TokenResult(BaseModel):
    token: ApiToken


class AuthPutResponse(BaseModel):
    result: TokenResult


class Timestamp(BaseModel):
    timestamp: PositiveInt


class AuthDeleteRequest(BaseModel):
    method: str = "revokeToken"
    params: Timestamp


class AssetsResult(BaseModel):
    assets: list[ApiAsset]


class CollectionAssetsGetResponse(BaseModel):
    result: AssetsResult
    next: Next | None = None


class CastsResult(BaseModel):
    casts: list[ApiCast]


class CastsGetResponse(BaseModel):
    result: CastsResult
    next: Next | None = None


class Parent(BaseModel):
    fid: PositiveInt
    hash: str


class CastsPostRequest(BaseModel):
    text: str
    embeds: list[AnyUrl] | None = None
    parent: Parent | None = None


class CastsPostResponse(BaseModel):
    result: CastContent


class CastGetResponse(BaseModel):
    result: CastContent


class CastHash(BaseModel):
    cast_hash: str = Field(..., alias="castHash")


class ReactionsResult(BaseModel):
    likes: list[ApiCastReaction]


class CastReactionsGetResponse(BaseModel):
    result: ReactionsResult
    next: Next | None = None


class CastReactionsPutRequest(BaseModel):
    type: str
    cast_fid: PositiveInt = Field(..., alias="castFid")
    cast_hash: str = Field(..., alias="castHash")


class CastReactionsPutResponse(BaseModel):
    result: ReactionsResult


class CastReactionsDeleteRequest(BaseModel):
    type: str
    cast_fid: PositiveInt = Field(..., alias="castFid")
    cast_hash: str = Field(..., alias="castHash")


class UsersResult(BaseModel):
    users: list[ApiUser]


class CastRecastersGetResponse(BaseModel):
    result: UsersResult
    next: Next | None = None


class CollectionResult(BaseModel):
    collection: ApiAssetCollection


class CollectionGetResponse(BaseModel):
    result: CollectionResult


class CollectionsResult(BaseModel):
    collections: list[ApiAssetCollection]


class UserCollectionsGetResponse(BaseModel):
    result: CollectionsResult
    next: Next | None = None


class EventsResult(BaseModel):
    events: list[ApiAssetEvent]


class CollectionActivityGetResponse(BaseModel):
    result: EventsResult
    next: Next | None = None


class CollectionOwnersGetResponse(BaseModel):
    result: UsersResult
    next: Next | None = None


class FollowsPutRequest(BaseModel):
    target_fid: PositiveInt = Field(..., alias="targetFid")


class StatusResponse(BaseModel):
    success: bool


class StatusResultResponse(BaseModel):
    result: StatusResponse


class FollowsDeleteRequest(BaseModel):
    target_fid: PositiveInt = Field(..., alias="targetFid")


class CustodyAddress(BaseModel):
    custody_address: str = Field(
        ..., alias="custodyAddress", regex=r"^0[xX][0-9a-fA-F]{40}$"
    )


class CustodyAddressGetResponse(BaseModel):
    result: CustodyAddress


class Likes(BaseModel):
    likes: list[ApiCastReaction]


class UserCastLikesGetResponse(BaseModel):
    result: Likes
    next: Next | None = None


class FollowersGetResponse(BaseModel):
    result: UsersResult
    next: Next | None = None


class FollowingGetResponse(BaseModel):
    result: UsersResult
    next: Next | None = None


class UsersGetResponse(BaseModel):
    result: UsersResult
    next: Next | None = None


class UserResult(BaseModel):
    user: ApiUser


class MeGetResponse(BaseModel):
    result: UserResult


class MentionNotification(BaseModel):
    type: str = "cast-mention"
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: CastContent


class ReplyNotification(BaseModel):
    type: str = "cast-reply"
    id: str
    timestamp: PositiveInt
    actor: ApiUser
    content: CastContent


class NotificationsResult(BaseModel):
    notifications: list[MentionNotification | ReplyNotification]


class MentionAndReplyNotificationsGetResponse(BaseModel):
    result: NotificationsResult
    next: Next | None = None


class RecastsPutResponse(BaseModel):
    result: CastHash


class UserGetResponse(BaseModel):
    result: UserResult


class UserByUsernameGetResponse(BaseModel):
    result: UserResult


class VerificationsResult(BaseModel):
    verifications: list[ApiVerification]


class VerificationsGetResponse(BaseModel):
    result: VerificationsResult
    next: Next | None = None


class WatchedCastsPutRequest(BaseModel):
    cast_fid: PositiveInt = Field(..., alias="castFid")
    cast_hash: str = Field(..., alias="castHash")


class WatchedCastsDeleteRequest(BaseModel):
    cast_fid: PositiveInt = Field(..., alias="castFid")
    cast_hash: str = Field(..., alias="castHash")


class CastLikesPutResponse(BaseModel):
    result: ReactionsResult


class CastLikesGetResponse(BaseModel):
    result: ReactionsResult
    next: Next | None = None
