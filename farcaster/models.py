from typing import Any, Dict, List, Optional, Type, Union

from fastapi_camelcase import CamelModel
from pydantic import AnyUrl
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, NoneStr, PositiveInt, conint, constr


class BaseModel(PydanticBaseModel):
    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        if hasattr(kwargs, "exclude_none"):
            _ignored = kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        allow_population_by_field_name = True


class ApiError(BaseModel):
    message: str


class ApiErrorResponse(BaseModel):
    errors: List[ApiError]


class ApiKeyStoreKey(BaseModel):
    key_id: str = Field(..., alias="keyId")
    type: str
    base64_public_key: str = Field(..., alias="base64PublicKey")
    base64_signature: str = Field(..., alias="base64Signature")
    timestamp: PositiveInt
    fid: Optional[PositiveInt] = None
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
    image: NoneStr = None
    logo: Optional[AnyUrl] = None
    use_large_image: Optional[bool] = Field(None, alias="useLargeImage")
    stripped_cast_text: NoneStr = Field(None, alias="strippedCastText")


class ApiCastAttachments(BaseModel):
    open_graph: Optional[List[ApiOpenGraphMetadata]] = Field(None, alias="openGraph")


class ApiOpenSeaNft(BaseModel):
    asset_contract_address: str
    token_id: str
    account_address: str


class ApiPfp(BaseModel):
    url: AnyUrl
    verified: bool


class Bio(BaseModel):
    text: str
    mentions: List[str]


class ApiProfile(BaseModel):
    bio: Bio


class ViewerContext(BaseModel):
    following: Optional[bool] = None
    followed_by: Optional[bool] = Field(None, alias="followedBy")
    can_send_direct_casts: Optional[bool] = Field(None, alias="canSendDirectCasts")


class ApiUser(BaseModel):
    fid: PositiveInt
    username: NoneStr = None
    display_name: NoneStr = Field(None, alias="displayName")
    registered_at: Optional[PositiveInt] = Field(None, alias="registeredAt")
    pfp: Optional[ApiPfp] = None
    profile: ApiProfile
    follower_count: int = Field(..., alias="followerCount")
    following_count: int = Field(..., alias="followingCount")
    referrer_username: NoneStr = Field(None, alias="referrerUsername")
    viewer_context: Optional[ViewerContext] = Field(None, alias="viewerContext")


class ApiUserPreferences(BaseModel):
    send_email_on_mention: Optional[bool] = Field(None, alias="sendEmailOnMention")
    send_email_on_reply: Optional[bool] = Field(None, alias="sendEmailOnReply")
    send_email_on_reaction: Optional[bool] = Field(None, alias="sendEmailOnReaction")
    send_email_on_follow: Optional[bool] = Field(None, alias="sendEmailOnFollow")
    send_weekly_update_emails: Optional[bool] = Field(
        None, alias="sendWeeklyUpdateEmails"
    )
    send_product_update_emails: Optional[bool] = Field(
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
    liked: Optional[bool] = None


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
    owner: Optional[ApiUser] = None
    last_sale: Optional[LastSale] = Field(None, alias="lastSale")
    mint: Optional[Mint] = None
    viewer_context: Optional[ViewerContext1] = Field(None, alias="viewerContext")


class ApiAssetGroup(BaseModel):
    collection: ApiAssetCollection
    assets: List[ApiAsset]


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
    events: List[ApiAssetEvent]


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
    username: NoneStr = None
    display_name: NoneStr = Field(None, alias="displayName")
    recast_hash: str = Field(..., alias="recastHash", regex=r"^0[xX][0-9a-fA-F]{64}$")


class Ancestors(BaseModel):
    count: int


class Replies(BaseModel):
    count: int


class Reactions(BaseModel):
    count: int


class Recasts(BaseModel):
    count: int
    recasters: Optional[List[ApiRecaster]] = None


class Watches(BaseModel):
    count: int


class ViewerContext2(BaseModel):
    reacted: Optional[bool] = None
    recast: Optional[bool] = None
    watched: Optional[bool] = None


class ApiCast(BaseModel):
    hash: str
    thread_hash: NoneStr = Field(None, alias="threadHash")
    parent_hash: NoneStr = Field(None, alias="parentHash")
    author: ApiUser
    text: str
    timestamp: PositiveInt
    mentions: Optional[List[ApiUser]] = None
    attachments: Optional[ApiCastAttachments] = None
    ancestors: Optional[Ancestors] = None
    replies: Replies
    reactions: Reactions
    recasts: Recasts
    watches: Watches
    deleted: Optional[bool] = None
    recast: Optional[bool] = None
    viewer_context: Optional[ViewerContext2] = Field(None, alias="viewerContext")


class ViewerContext3(BaseModel):
    sender: bool


class ApiDirectCast(BaseModel):
    sender: ApiUser
    text: str
    timestamp: PositiveInt
    viewer_context: Optional[ViewerContext3] = Field(None, alias="viewerContext")


class ApiDirectCastConversation(BaseModel):
    conversation_id: str = Field(..., alias="conversationId")
    participants: List[ApiUser]
    last_direct_cast: ApiDirectCast = Field(..., alias="lastDirectCast")
    timestamp: PositiveInt


class ApiUnseenConversation(BaseModel):
    conversation_id: str = Field(..., alias="conversationId")
    participant_fids: List[int] = Field(..., alias="participantFids")
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
    __root__: Union[
        ApiNotificationCastReaction,
        ApiNotificationCastMention,
        ApiNotificationCastReply,
        ApiNotificationFollow,
        ApiNotificationRecast,
        ApiNotificationWatchedCastReply,
    ] = Field(..., title="ApiNotification")


class ApiCastReactionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationCastReaction] = Field(..., alias="previewItems")


class ApiCastMentionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationCastMention] = Field(..., alias="previewItems")


class ApiCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationCastReply] = Field(..., alias="previewItems")


class ApiFollowNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationFollow] = Field(..., alias="previewItems")


class ApiRecastNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationRecast] = Field(..., alias="previewItems")


class ApiWatchedCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt = Field(..., alias="latestTimestamp")
    total_item_count: int = Field(..., alias="totalItemCount")
    preview_items: List[ApiNotificationWatchedCastReply] = Field(
        ..., alias="previewItems"
    )


class ApiNotificationGroup(BaseModel):
    __root__: Union[
        ApiCastReactionNotificationGroup,
        ApiCastMentionNotificationGroup,
        ApiCastReplyNotificationGroup,
        ApiFollowNotificationGroup,
        ApiRecastNotificationGroup,
        ApiWatchedCastReplyNotificationGroup,
    ] = Field(..., title="ApiNotificationGroup")


class ApiCastFeedItem(BaseModel):
    id: str
    timestamp: PositiveInt
    cast: ApiCast
    replies: Optional[List[ApiCast]] = None
    other_participants: List[ApiUser] = Field(..., alias="otherParticipants")


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
    __root__: Union[ViewCastPushNotification, UnreadDirectCastPushNotification] = Field(
        ..., title="PushNotificationPayload"
    )


class Result(BaseModel):
    status: str


class HealthcheckGetResponse(BaseModel):
    result: Result


class Next(BaseModel):
    cursor: NoneStr = None


class EventsResult(BaseModel):
    events: List[ApiAssetEvent]


class AssetEventsGetResponse(BaseModel):
    result: EventsResult
    next: Optional[Next] = None


class AssetResult(BaseModel):
    asset: ApiAsset


class AssetGetResponse(BaseModel):
    result: AssetResult


class AuthParams(CamelModel):
    timestamp: PositiveInt
    expires_at: Optional[PositiveInt] = Field(None, alias="expiresAt")


class AuthPutRequest(BaseModel):
    method: str = "generateToken"
    params: AuthParams


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
    assets: List[ApiAsset]


class CollectionAssetsGetResponse(BaseModel):
    result: AssetsResult
    next: Optional[Next] = None


class CastsResult(BaseModel):
    casts: List[ApiCast]


class CastsGetResponse(BaseModel):
    result: CastsResult
    next: Optional[Next] = None


class Parent(BaseModel):
    fid: PositiveInt
    hash: str


class CastsPostRequest(BaseModel):
    text: str
    embeds: Optional[List[AnyUrl]] = None
    parent: Optional[Parent] = None


class CastsPostResponse(BaseModel):
    result: CastContent


class CastGetResponse(BaseModel):
    result: CastContent


class CastHash(BaseModel):
    cast_hash: str = Field(..., alias="castHash")


class ReactionsResult(BaseModel):
    likes: List[ApiCastReaction]


class CastReactionsGetResponse(BaseModel):
    result: ReactionsResult
    next: Optional[Next] = None


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
    users: List[ApiUser]


class CastRecastersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


class CollectionResult(BaseModel):
    collection: ApiAssetCollection


class CollectionGetResponse(BaseModel):
    result: CollectionResult


class CollectionsResult(BaseModel):
    collections: List[ApiAssetCollection]


class UserCollectionsGetResponse(BaseModel):
    result: CollectionsResult
    next: Optional[Next] = None


class CollectionActivityGetResponse(BaseModel):
    result: EventsResult
    next: Optional[Next] = None


class CollectionOwnersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


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
    likes: List[ApiCastReaction]


class UserCastLikesGetResponse(BaseModel):
    result: Likes
    next: Optional[Next] = None


class FollowersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


class FollowingGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


class UsersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


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
    notifications: List[Union[MentionNotification, ReplyNotification]]


class MentionAndReplyNotificationsGetResponse(BaseModel):
    result: NotificationsResult
    next: Optional[Next] = None


class RecastsPutResponse(BaseModel):
    result: CastHash


class UserGetResponse(BaseModel):
    result: UserResult


class UserByUsernameGetResponse(BaseModel):
    result: UserResult


class VerificationsResult(BaseModel):
    verifications: List[ApiVerification]


class VerificationsGetResponse(BaseModel):
    result: VerificationsResult
    next: Optional[Next] = None


class CastLikesPutResponse(BaseModel):
    result: ReactionsResult


class CastLikesGetResponse(BaseModel):
    result: ReactionsResult
    next: Optional[Next] = None
