from typing import List, Optional, Union

from humps import camelize
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, PositiveInt, RootModel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)


class ApiError(BaseModel):
    message: str


class ApiErrorResponse(BaseModel):
    errors: List[ApiError]


class ApiKeyStoreKey(BaseModel):
    key_id: str
    type: str
    base64_public_key: str
    base64_signature: str
    timestamp: PositiveInt
    fid: Optional[PositiveInt] = None
    device_id: Optional[str] = None
    device_name: Optional[str] = None


class ApiToken(BaseModel):
    secret: str
    expires_at: PositiveInt


class ApiOpenGraphMetadata(BaseModel):
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    image: Optional[str] = None
    logo: Optional[str] = None
    use_large_image: Optional[bool] = None
    stripped_cast_text: Optional[str] = None


class ApiCastAttachments(BaseModel):
    open_graph: Optional[List[ApiOpenGraphMetadata]] = None


class ApiOpenSeaNft(BaseModel):
    asset_contract_address: str
    token_id: str
    account_address: str


class ApiPfp(BaseModel):
    url: str
    verified: Optional[bool] = None


class Bio(BaseModel):
    text: str
    mentions: Optional[List[str]] = None


class ApiProfile(BaseModel):
    bio: Bio


class ViewerContext(BaseModel):
    following: Optional[bool] = None
    followed_by: Optional[bool] = None
    can_send_direct_casts: Optional[bool] = None


class ApiUser(BaseModel):
    fid: PositiveInt
    username: Optional[str] = None
    display_name: Optional[str] = None
    registered_at: Optional[PositiveInt] = None
    pfp: Optional[ApiPfp] = None
    profile: ApiProfile
    follower_count: int
    following_count: int
    referrer_username: Optional[str] = None
    viewer_context: Optional[ViewerContext] = None


class ApiUserPreferences(BaseModel):
    send_email_on_mention: Optional[bool] = None
    send_email_on_reply: Optional[bool] = None
    send_email_on_reaction: Optional[bool] = None
    send_email_on_follow: Optional[bool] = None
    send_weekly_update_emails: Optional[bool] = None
    send_product_update_emails: Optional[bool] = None


class ApiAssetCollection(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    item_count: int
    owner_count: int
    farcaster_owner_count: int
    image_url: str
    floor_price: Optional[str] = None
    volume_traded: str
    external_url: Optional[str] = None
    open_sea_url: str
    twitter_username: Optional[str] = None
    schema_name: Optional[str] = None


class LastSale(BaseModel):
    price: str
    date: str


class Mint(BaseModel):
    date: str
    transaction_hash: str


class ViewerContext1(BaseModel):
    liked: Optional[bool] = None


class ApiAsset(BaseModel):
    id: str
    name: str
    contract_address: str
    token_id: str
    image_url: str
    external_url: Optional[str] = None
    open_sea_url: str
    like_count: int
    uri: str
    collection: ApiAssetCollection
    owner: Optional[ApiUser] = None
    last_sale: Optional[LastSale] = None
    mint: Optional[Mint] = None
    viewer_context: Optional[ViewerContext1] = None


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
    latest_timestamp: PositiveInt
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
    cast_hash: str = Field(..., pattern=r"^0x[0-9a-fA-F]{40}$")


class ApiNewCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent


class ApiTopCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent


class ApiTrendingCollection(BaseModel):
    collection: ApiAssetCollection
    first_event: ApiAssetEvent
    recent_unique_users_count: int


class ApiRecaster(BaseModel):
    fid: PositiveInt
    username: Optional[str] = None
    display_name: Optional[str] = None


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


class ParentSource(BaseModel):
    type: str
    url: str


class ApiCastUrlEmbed(BaseModel):
    type: str
    open_graph: ApiOpenGraphMetadata
    user: Optional[ApiUser] = None
    asset: Optional[ApiAsset] = None
    collection: Optional[ApiAssetCollection] = None


class ApiCastImageEmbed(BaseModel):
    type: str
    url: str
    sourceUrl: str
    alt: str


class ApiCastUnknownEmbed(BaseModel):
    type: str
    source: str


class ApiCastEmbeds(BaseModel):
    images: List[ApiCastImageEmbed]
    urls: List[ApiCastUrlEmbed]
    unknowns: List[ApiCastUnknownEmbed]


class ApiCast(BaseModel):
    hash: str
    thread_hash: Optional[str] = None
    parent_hash: Optional[str] = None
    author: ApiUser
    parent_author: Optional[ApiUser] = None
    parent_source: Optional[ParentSource] = None
    text: str
    timestamp: PositiveInt
    mentions: Optional[List[ApiUser]] = None
    attachments: Optional[ApiCastAttachments] = None
    embeds: Optional[ApiCastEmbeds] = None
    ancestors: Optional[Ancestors] = None
    replies: Replies
    reactions: Reactions
    recasts: Recasts
    watches: Watches
    deleted: Optional[bool] = None
    recast: Optional[bool] = None
    viewer_context: Optional[ViewerContext2] = None


class ViewerContext3(BaseModel):
    sender: bool


class ApiDirectCast(BaseModel):
    sender: ApiUser
    text: str
    timestamp: PositiveInt
    viewer_context: Optional[ViewerContext3] = None


class ApiDirectCastConversation(BaseModel):
    conversation_id: str
    participants: List[ApiUser]
    last_direct_cast: ApiDirectCast
    timestamp: PositiveInt


class ApiUnseenConversation(BaseModel):
    conversation_id: str
    participant_fids: List[int]
    last_direct_cast_timestamp: PositiveInt


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
    recasted_cast: ApiCast


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


class ApiNotification(
    RootModel[
        Union[
            ApiNotificationCastReaction,
            ApiNotificationCastMention,
            ApiNotificationCastReply,
            ApiNotificationFollow,
            ApiNotificationRecast,
            ApiNotificationWatchedCastReply,
        ]
    ]
):
    pass


class ApiCastReactionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationCastReaction]


class ApiCastMentionNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationCastMention]


class ApiCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationCastReply]


class ApiFollowNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationFollow]


class ApiRecastNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationRecast]


class ApiWatchedCastReplyNotificationGroup(BaseModel):
    id: str
    type: str
    latest_timestamp: PositiveInt
    total_item_count: int
    preview_items: List[ApiNotificationWatchedCastReply]


class ApiNotificationGroup(
    RootModel[
        Union[
            ApiCastReactionNotificationGroup,
            ApiCastMentionNotificationGroup,
            ApiCastReplyNotificationGroup,
            ApiFollowNotificationGroup,
            ApiRecastNotificationGroup,
            ApiWatchedCastReplyNotificationGroup,
        ]
    ]
):
    pass


class ApiCastFeedItem(BaseModel):
    id: str
    timestamp: PositiveInt
    cast: ApiCast
    replies: Optional[List[ApiCast]] = None
    other_participants: List[ApiUser]


class ViewCastPushNotification(BaseModel):
    id: str
    type: str
    merkle_root: str
    thread_merkle_root: str
    cast_fid: float
    cast_hash: str


class UnreadDirectCastPushNotification(BaseModel):
    id: str
    type: str


class PushNotificationPayload(
    RootModel[Union[ViewCastPushNotification, UnreadDirectCastPushNotification]]
):
    pass


class Result(BaseModel):
    status: str


class HealthcheckGetResponse(BaseModel):
    result: Result


class Next(BaseModel):
    cursor: Optional[str] = None


class EventsResult(BaseModel):
    events: List[ApiAssetEvent]


class IterableEventsResult(BaseModel):
    events: List[ApiAssetEvent]
    cursor: Optional[str] = None


class AssetEventsGetResponse(BaseModel):
    result: EventsResult
    next: Optional[Next] = None


class AssetResult(BaseModel):
    asset: ApiAsset


class AssetGetResponse(BaseModel):
    result: AssetResult


class AuthParams(BaseModel):
    timestamp: PositiveInt
    expires_at: PositiveInt


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


class CastsResult(BaseModel):
    casts: List[ApiCast]


class IterableCastsResult(BaseModel):
    casts: List[ApiCast]
    cursor: Optional[str] = None


class CastsGetResponse(BaseModel):
    result: CastsResult
    next: Optional[Next] = None


class Parent(BaseModel):
    fid: PositiveInt
    hash: str


class CastsPostRequest(BaseModel):
    text: str
    embeds: Optional[List[str]] = None
    parent: Optional[Parent] = None
    channel_key: Optional[str] = None


class CastsPostResponse(BaseModel):
    result: CastContent


class CastGetResponse(BaseModel):
    result: CastContent


class CastHash(BaseModel):
    cast_hash: str


class ReactionsResult(BaseModel):
    likes: List[ApiCastReaction]


class IterableReactionsResult(BaseModel):
    likes: List[ApiCastReaction]
    cursor: Optional[str] = None


class ReactionsPutResult(BaseModel):
    like: ApiCastReaction


class CastReactionsGetResponse(BaseModel):
    result: ReactionsResult
    next: Optional[Next] = None


class CastReactionsPutRequest(BaseModel):
    type: str
    cast_fid: PositiveInt
    cast_hash: str


class CastReactionsPutResponse(BaseModel):
    result: ReactionsPutResult


class CastReactionsDeleteRequest(BaseModel):
    type: str
    cast_fid: PositiveInt
    cast_hash: str


class UsersResult(BaseModel):
    users: List[ApiUser]


class IterableUsersResult(BaseModel):
    users: List[ApiUser]
    cursor: Optional[str] = None


class CastRecastersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


class CollectionsResult(BaseModel):
    collections: List[ApiAssetCollection]


class IterableCollectionsResult(BaseModel):
    collections: List[ApiAssetCollection]
    cursor: Optional[str] = None


class UserCollectionsGetResponse(BaseModel):
    result: CollectionsResult
    next: Optional[Next] = None


class CollectionOwnersGetResponse(BaseModel):
    result: UsersResult
    next: Optional[Next] = None


class FollowsPutRequest(BaseModel):
    target_fid: PositiveInt


class StatusContent(BaseModel):
    success: bool


class StatusResponse(BaseModel):
    result: StatusContent


class FollowsDeleteRequest(BaseModel):
    target_fid: PositiveInt


class CustodyAddress(BaseModel):
    custody_address: str = Field(..., pattern=r"^0[xX][0-9a-fA-F]{40}$")


class CustodyAddressGetResponse(BaseModel):
    result: CustodyAddress


class Likes(BaseModel):
    likes: List[ApiCastReaction]


class IterableLikes(BaseModel):
    likes: List[ApiCastReaction]
    cursor: Optional[str] = None


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


class IterableNotificationsResult(BaseModel):
    notifications: List[Union[MentionNotification, ReplyNotification]]
    cursor: Optional[str] = None


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


class IterableVerificationsResult(BaseModel):
    verifications: List[ApiVerification]
    cursor: Optional[str] = None


class VerificationsGetResponse(BaseModel):
    result: VerificationsResult
    next: Optional[Next] = None


class CastLikesPutResponse(BaseModel):
    result: ReactionsResult


class CastLikesGetResponse(BaseModel):
    result: ReactionsResult
    next: Optional[Next] = None
