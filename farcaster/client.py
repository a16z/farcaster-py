from typing import Any, Dict, Iterator, Optional

import base64
import logging
import time

import canonicaljson
import requests
from eth_account.account import Account
from eth_account.datastructures import SignedMessage
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from pydantic import PositiveInt
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from farcaster.config import *
from farcaster.models import *
from farcaster.utils.stream_generator import stream_generator


class Warpcast:
    """The Warpcast class is a wrapper around the Farcaster API.
    It also provides a number of helpful methods and utilities for interacting with the protocol.
    Pydantic models are used under the hood to validate the data returned from the API.
    """

    config: ConfigurationParams
    wallet: Optional[LocalAccount]
    access_token: Optional[str]
    expires_at: Optional[PositiveInt]
    rotation_duration: PositiveInt
    session: requests.Session

    def __init__(
        self,
        mnemonic: Optional[str] = None,
        private_key: Optional[str] = None,
        access_token: Optional[str] = None,
        expires_at: Optional[PositiveInt] = None,
        rotation_duration: PositiveInt = 10,
        **data: Any,
    ):
        self.config = ConfigurationParams(**data)
        self.wallet = get_wallet(mnemonic, private_key)
        self.access_token = access_token
        self.expires_at = expires_at
        self.rotation_duration = rotation_duration
        self.session = requests.Session()
        self.session.mount(
            self.config.base_path,
            HTTPAdapter(
                max_retries=Retry(
                    total=2, backoff_factor=1, status_forcelist=[520, 413, 429, 503]
                )
            ),
        )
        if self.access_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )
            if not self.expires_at:
                self.expires_at = 33228645430000  # 3000-01-01

        elif not self.wallet:
            raise Exception("No wallet or access token provided")
        else:
            self.create_new_auth_token(expires_in=self.rotation_duration)

    def get_base_path(self):
        return self.config.base_path

    def get_base_options(self):
        return self.config.base_options

    def _get(
        self,
        path: str,
        params: Dict[Any, Any] = {},
        json: Dict[Any, Any] = {},
        headers: Dict[Any, Any] = {},
    ) -> Dict[Any, Any]:
        self._check_auth_header()
        logging.debug(f"GET {path} {params} {json} {headers}")
        response: Dict[Any, Any] = self.session.get(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response

    def _post(
        self,
        path: str,
        params: Dict[Any, Any] = {},
        json: Dict[Any, Any] = {},
        headers: Dict[Any, Any] = {},
    ) -> Dict[Any, Any]:
        self._check_auth_header()
        logging.debug(f"POST {path} {params} {json} {headers}")
        response: Dict[Any, Any] = self.session.post(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response

    def _put(
        self,
        path: str,
        params: Dict[Any, Any] = {},
        json: Dict[Any, Any] = {},
        headers: Dict[Any, Any] = {},
    ) -> Dict[Any, Any]:
        self._check_auth_header()
        logging.debug(f"PUT {path} {params} {json} {headers}")
        response: Dict[Any, Any] = self.session.put(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response

    def _delete(
        self,
        path: str,
        params: Dict[Any, Any] = {},
        json: Dict[Any, Any] = {},
        headers: Dict[Any, Any] = {},
    ) -> Dict[Any, Any]:
        self._check_auth_header()
        logging.debug(f"DELETE {path} {params} {json} {headers}")
        response: Dict[Any, Any] = self.session.delete(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])  # pragma: no cover
        return response

    def _check_auth_header(self):
        assert self.expires_at
        if self.expires_at < now_ms() + 1000:
            self.create_new_auth_token(expires_in=self.rotation_duration)

    def get_healthcheck(self) -> bool:
        """Check if API is up and running

        Returns:
            bool: Status of the API
        """
        response = self.session.get("https://api.warpcast.com/healthcheck")
        return response.ok

    def get_asset(self, token_id: int) -> AssetResult:
        """Get asset information

        Args:
            token_id (int): token ID

        Returns:
            AssetResult: token information
        """
        response = self._get("asset", {"token_id": token_id})
        return AssetGetResponse(**response).result

    def get_asset_events(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableEventsResult:
        """Get events for a given asset

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): events to receive, defaults
                to 25

        Returns:
            IterableEventsResult: Returns the EventsResult model with an optional cursor
        """
        response = AssetEventsGetResponse(
            **self._get(
                "asset-events",
                params={"cursor": cursor, "limit": limit},
            )
        )
        return IterableEventsResult(
            events=response.result.events, cursor=getattr(response.next, "cursor", None)
        )

    def put_auth(self, auth_params: AuthParams) -> TokenResult:
        """Generate a custody bearer token and use it to generate an access token

        Args:
            auth_params (AuthParams): _description_

        Returns:
            TokenResult: _description_
        """
        header = self.generate_custody_auth_header(auth_params)
        body = AuthPutRequest(params=auth_params)
        response = requests.put(
            self.config.base_path + "auth",
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers={"Authorization": header},
        ).json()
        return AuthPutResponse(**response).result

    def delete_auth(self) -> StatusContent:
        """Delete an access token

        Returns:
            StatusContent: Status of the deletion
        """
        timestamp = now_ms()
        body = AuthDeleteRequest(params=Timestamp(timestamp=timestamp))
        response = self._delete(
            "auth",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def get_cast_likes(
        self,
        cast_hash: str,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableReactionsResult:
        """Get the likes for a given cast

        Args:
            cast_hash (str): cast hash
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableReactionsResult: Model containing the likes with an optional cursor
        """
        likes: List[ApiCastReaction] = []
        while True:
            response = self._get(
                "cast-likes",
                params={
                    "castHash": cast_hash,
                    "cursor": cursor,
                    "limit": min(limit, 100),
                },
            )
            response_model = CastReactionsGetResponse(**response)
            if response_model.result.likes:
                likes = response_model.result.likes
            if not response_model.next or len(likes) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableReactionsResult(
            likes=likes[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def like_cast(self, cast_hash: str) -> ReactionsPutResult:
        """Like a given cast

        Args:
            cast_hash (str): hash of the cast to like

        Returns:
            ReactionsPutResult: Result of liking the cast
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._put(
            "cast-likes",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return CastReactionsPutResponse(**response).result

    def delete_cast_likes(self, cast_hash: str) -> StatusContent:
        """Remove a like from a cast

        Args:
            cast_hash (str): hash of the cast to unlike

        Returns:
            StatusContent: Status of the deletion
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._delete(
            "cast-likes",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def get_cast_recasters(
        self,
        cast_hash: str,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableUsersResult:
        """Get the recasters for a given cast

        Args:
            cast_hash (str): cast hash
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableUsersResult: Model containing the recasters with an optional cursor
        """
        users: List[ApiUser] = []
        while True:
            response = self._get(
                "cast-recasters",
                params={
                    "castHash": cast_hash,
                    "cursor": cursor,
                    "limit": min(limit, 100),
                },
            )
            response_model = CastRecastersGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if not response_model.next or len(users) >= limit:
                break
        return IterableUsersResult(
            users=users, cursor=getattr(response_model.next, "cursor", None)
        )

    def get_cast(
        self,
        hash: str,
    ) -> CastContent:
        """Get a specific cast

        Args:
            hash (str): cast hash

        Returns:
            CastContent: The cast content
        """
        response = self._get(
            "cast",
            params={"hash": hash},
        )
        return CastGetResponse(**response).result

    def get_all_casts_in_thread(
        self,
        thread_hash: str,
    ) -> CastsResult:
        """Get all casts in a thread

        Args:
            thread_hash (str): hash of the thread

        Returns:
            CastsResult: Model containing the casts
        """
        response = self._get(
            "all-casts-in-thread",
            params={"threadHash": thread_hash},
        )
        return CastsGetResponse(**response).result

    def get_casts(
        self,
        fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableCastsResult:
        """Get the casts for a given fid of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableCastsResult: Model containing the casts with an optional cursor
        """
        casts: List[ApiCast] = []
        while True:
            response = self._get(
                "casts",
                params={"fid": fid, "cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = CastsGetResponse(**response)
            if response_model.result.casts:
                casts.extend(response_model.result.casts)
            if not response_model.next or len(casts) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableCastsResult(
            casts=casts[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def post_cast(
        self,
        text: str,
        embeds: Optional[List[str]] = None,
        parent: Optional[Parent] = None,
    ) -> CastContent:
        """Post a cast to Farcaster

        Args:
            text (str): text of the cast
            embeds (Optional[List[str]], optional): list of embeds, defaults to None
            parent (Optional[Parent], optional): parent of the cast, defaults to None

        Returns:
            CastContent: The result of posting the cast
        """
        body = CastsPostRequest(text=text, embeds=embeds, parent=parent)
        response = self._post(
            "casts",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return CastsPostResponse(**response).result

    def delete_cast(self, cast_hash: str) -> StatusContent:
        """Delete a cast

        Args:
            cast_hash (str): the hash of the cast to delete

        Returns:
            StatusContent: Status of the deletion
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._delete(
            "casts",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def get_collection_owners(
        self,
        collection_id: str,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableUsersResult:
        """Get the owners of an OpenSea collection

        Args:
            collection_id (str): OpenSea collection ID
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableUsersResult: model containing users with an optional cursor
        """
        users: List[ApiUser] = []
        while True:
            response = self._get(
                "collection-owners",
                params={
                    "collectionId": collection_id,
                    "cursor": cursor,
                    "limit": min(limit, 100),
                },
            )
            response_model = CollectionOwnersGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if not response_model.next or len(users) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableUsersResult(
            users=users[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def get_followers(
        self,
        fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableUsersResult:
        """Get the followers of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableUsersResult: model containing users with an optional cursor
        """
        users: List[ApiUser] = []
        while True:
            response = self._get(
                "followers",
                params={"fid": fid, "cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = FollowersGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if not response_model.next or len(users) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableUsersResult(
            users=users[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def get_all_followers(self, fid: Optional[int] = None) -> UsersResult:
        """Get all followers of a user by iterating through the next cursors
        Args:
            fid (int): Farcaster ID of the user
        Returns:
            UsersResult: model containing users
        """
        users: List[ApiUser] = []
        cursor = None
        limit = 100
        if fid is None:
            fid = self.get_me().fid
        while True:
            response = self._get(
                "followers",
                params={"fid": fid, "cursor": cursor, "limit": limit},
            )
            response_model = FollowersGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if response_model.next is None:
                break
            cursor = response_model.next.cursor
        return UsersResult(users=users)

    def get_following(
        self,
        fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableUsersResult:
        """Get the users a user is following

        Args:
            fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableUsersResult: model containing users with an optional cursor
        """
        users: List[ApiUser] = []
        while True:
            response = self._get(
                "following",
                params={"fid": fid, "cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = FollowingGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if not response_model.next or len(users) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableUsersResult(
            users=users[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def get_all_following(self, fid: Optional[int] = None) -> UsersResult:
        """Get all the users a user is following by iterating through the next cursors

        Args:
            fid (int): Farcaster ID of the user

        Returns:
            UsersResult: model containing users
        """
        users: List[ApiUser] = []
        cursor = None
        limit = 100
        if fid is None:
            fid = self.get_me().fid
        while True:
            response = self._get(
                "following",
                params={"fid": fid, "cursor": cursor, "limit": limit},
            )
            response_model = FollowingGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if response_model.next is None:
                break
            cursor = response_model.next.cursor
        return UsersResult(users=users)

    def follow_user(self, fid: PositiveInt) -> StatusContent:
        """Follow a user

        Args:
            fid (PositiveInt): Farcaster ID of the user to follow

        Returns:
            StatusContent: Status of the follow
        """
        body = FollowsPutRequest(target_fid=fid)
        response = self._put(
            "follows",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def unfollow_user(self, fid: PositiveInt) -> StatusContent:
        """Unfollow a user

        Args:
            fid (PositiveInt): Farcaster ID of the user to unfollow

        Returns:
            StatusContent: Status of the unfollow
        """
        body = FollowsDeleteRequest(target_fid=fid)
        response = self._delete(
            "follows",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def get_me(self) -> ApiUser:
        """Get the current user

        Returns:
            ApiUser: model containing the current user
        """
        response = self._get(
            "me",
        )
        response_model = MeGetResponse(**response).result
        self.config.username = response_model.user.username
        return response_model.user

    def get_mention_and_reply_notifications(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableNotificationsResult:
        """Get mention and reply notifications

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableNotificationsResult: model containing notifications with an optional cursor
        """
        notifications: List[Union[MentionNotification, ReplyNotification]] = []
        while True:
            response = self._get(
                "mention-and-reply-notifications",
                params={"cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = MentionAndReplyNotificationsGetResponse(**response)
            if response_model.result.notifications:
                notifications.extend(response_model.result.notifications)
            if not response_model.next or len(notifications) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableNotificationsResult(
            notifications=notifications[:limit],
            cursor=getattr(response_model.next, "cursor", None),
        )

    def _recent_notifications_list(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> List[Union[MentionNotification, ReplyNotification]]:
        """Get mention and reply notifications as a list

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            List[Union[MentionNotification, ReplyNotification]]: list of notifications
        """
        return self.get_mention_and_reply_notifications(
            cursor=cursor, limit=limit
        ).notifications

    def stream_notifications(
        self, **stream_options: Any
    ) -> Iterator[Optional[Union[MentionNotification, ReplyNotification]]]:
        """Stream all recent notifications

        Possible stream options:
            ``pause_after``: ``Optional[int]`` = ``None``, The number of times to call the API without finding a new item

            ``skip_existing``: ``bool`` = ``False``, If ``True``, skip items that existed before the stream was created

            ``max_counter``: ``PositiveInt`` = ``16``, The maximum number of seconds to wait between calls to the API

        Args:
            **stream_options: stream options

        Returns:
            Iterator[Optional[Union[MentionNotification, ReplyNotification]]]: iterator of notifications. Returns none if pause_after is reached
        """
        return stream_generator(
            self._recent_notifications_list,
            attribute_name="id",
            limit=20,
            **stream_options,
        )

    def recast(self, cast_hash: str) -> CastHash:
        """Recast a cast

        Args:
            cast_hash (str): the cast hash

        Returns:
            CastHash: model containing the cast hash
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._put(
            "recasts",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return RecastsPutResponse(**response).result

    def delete_recast(self, cast_hash: str) -> StatusContent:
        """Delete a recast

        Args:
            cast_hash (str): the cast hash

        Returns:
            StatusContent: Status of the recast deletion
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._delete(
            "recasts",
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        return StatusResponse(**response).result

    def get_user(self, fid: int) -> ApiUser:
        """Get a user

        Args:
            fid (int): Farcaster ID of the user

        Returns:
            ApiUser: model containing the user
        """
        response = self._get(
            "user",
            params={"fid": fid},
        )
        return UserGetResponse(**response).result.user

    def get_user_by_username(
        self,
        username: str,
    ) -> ApiUser:
        """Get a user by username

        Args:
            username (str): username of the user

        Returns:
            ApiUser: model containing the user
        """
        response = self._get(
            "user-by-username",
            params={"username": username},
        )
        return UserByUsernameGetResponse(**response).result.user

    def get_user_by_verification(
        self,
        address: str,
    ) -> ApiUser:
        """Get a user by verification address

        Args:
            address (str): address of the user

        Returns:
            ApiUser: model containing the user
        """
        response = self._get(
            "user-by-verification",
            params={"address": address},
        )
        return UserByUsernameGetResponse(**response).result.user

    def get_user_collections(
        self,
        owner_fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableCollectionsResult:
        """Get the collections of a user

        Args:
            owner_fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableCollectionsResult: model containing collections with an optional cursor
        """
        collections: List[ApiAssetCollection] = []
        while True:
            response = self._get(
                "user-collections",
                params={
                    "ownerFid": owner_fid,
                    "cursor": cursor,
                    "limit": min(limit, 100),
                },
            )
            response_model = UserCollectionsGetResponse(**response)
            if response_model.result.collections:
                collections.extend(response_model.result.collections)
            if not response_model.next or len(collections) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableCollectionsResult(
            collections=collections[:limit],
            cursor=getattr(response_model.next, "cursor", None),
        )

    def get_verifications(
        self,
        fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableVerificationsResult:
        """Get the verifications of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            IterableVerificationsResult: model containing verifications with an optional cursor
        """
        response = VerificationsGetResponse(
            **self._get(
                "verifications",
                params={"fid": fid, "cursor": cursor, "limit": limit},
            )
        )
        return IterableVerificationsResult(
            verifications=response.result.verifications,
            cursor=getattr(response.next, "cursor", None),
        )

    def get_recent_users(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableUsersResult:
        """Get recent users

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableUsersResult: model containing users with an optional cursor
        """
        users: List[ApiUser] = []
        while True:
            response = self._get(
                "recent-users",
                params={"cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = UsersGetResponse(**response)
            if response_model.result.users:
                users.extend(response_model.result.users)
            if not response_model.next or len(users) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableUsersResult(
            users=users[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def _recent_users_list(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> List[ApiUser]:
        """Get recent users as a list

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            List[ApiUser]: list of users
        """
        return self.get_recent_users(cursor=cursor, limit=limit).users

    def stream_users(self, **stream_options: Any) -> Iterator[Optional[ApiUser]]:
        """Stream all recent users.

        Possible stream options:
            ``pause_after``: ``Optional[int]`` = ``None``, The number of times to call the API without finding a new item

            ``skip_existing``: ``bool`` = ``False``, If ``True``, skip items that existed before the stream was created

            ``max_counter``: ``PositiveInt`` = ``16``, The maximum number of seconds to wait between calls to the API

        Args:
            **stream_options: stream options


        Returns:
            Iterator[Optional[ApiUser]]: iterator of users. Returns none if pause_after is reached
        """
        return stream_generator(
            self._recent_users_list, attribute_name="fid", limit=20, **stream_options
        )

    def get_custody_address(
        self,
        username: Optional[str] = None,
        fid: Optional[int] = None,
    ) -> CustodyAddress:
        """Get the custody address of a user

        Args:
            username (Optional[str], optional): username of a user, defaults
                to None
            fid (Optional[int], optional): Farcaster ID, defaults to
                None

        Returns:
            CustodyAddress: model containing the custody address
        """
        assert username or fid, "fname or fid must be provided"
        response = self._get(
            "custody-address",
            params={"fname": username, "fid": fid},
        )
        return CustodyAddressGetResponse(**response).result

    def get_user_cast_likes(
        self,
        fid: int,
        cursor: Optional[str] = None,
        limit: PositiveInt = 25,
    ) -> IterableLikes:
        """Get the likes of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25, otherwise min(limit, 100)

        Returns:
            IterableLikes: model containing likes with an optional cursor
        """
        likes: List[ApiCastReaction] = []
        while True:
            response = self._get(
                "user-cast-likes",
                params={"fid": fid, "cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = UserCastLikesGetResponse(**response)
            if response_model.result.likes:
                likes.extend(response_model.result.likes)
            if not response_model.next or len(likes) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableLikes(
            likes=likes[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def get_recent_casts(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 100,
    ) -> IterableCastsResult:
        """Get all recent casts

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 100

        Returns:
            IterableCastsResult: model containing casts with an optional cursor
        """
        casts: List[ApiCast] = []
        while True:
            response = self._get(
                "recent-casts",
                params={"cursor": cursor, "limit": min(limit, 100)},
            )
            response_model = CastsGetResponse(**response)
            if response_model.result.casts:
                casts.extend(response_model.result.casts)
            if not response_model.next or len(casts) >= limit:
                break
            cursor = response_model.next.cursor
        return IterableCastsResult(
            casts=casts[:limit], cursor=getattr(response_model.next, "cursor", None)
        )

    def _recent_casts_lists(
        self,
        cursor: Optional[str] = None,
        limit: PositiveInt = 100,
    ) -> List[ApiCast]:
        """Get all recent casts and return them as a list

        Args:
            cursor (Optional[str], optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 100

        Returns:
            List[ApiCast]: list of casts
        """
        return self.get_recent_casts(cursor=cursor, limit=limit).casts

    def stream_casts(self, **stream_options: Any) -> Iterator[Optional[ApiCast]]:
        """Stream all recent casts

        Possible stream options:
            ``pause_after``: ``Optional[int]`` = ``None``, The number of times to call the API without finding a new item

            ``skip_existing``: ``bool`` = ``False``, If ``True``, skip items that existed before the stream was created

            ``max_counter``: ``PositiveInt`` = ``16``, The maximum number of seconds to wait between calls to the API

        Args:
            **stream_options: stream options

        Returns:
            Iterator[Optional[ApiCast]]: iterator of casts. Returns none if pause_after is reached
        """
        return stream_generator(
            self._recent_casts_lists, attribute_name="hash", limit=50, **stream_options
        )

    def create_new_auth_token(self, expires_in: PositiveInt = 10) -> str:
        """Create a new access token for a user from the wallet credentials

        Args:
            expires_in (PositiveInt): Expiration length of the token in minutes,
                defaults to 10 minutes

        Returns:
            str: access token
        """
        now = int(time.time())
        auth_params = AuthParams(
            timestamp=now * 1000, expires_at=(now + (expires_in * 60)) * 1000
        )
        logging.debug(f"Creating new auth token with params: {auth_params}")
        response = self.put_auth(auth_params)
        self.access_token = response.token.secret
        self.expires_at = auth_params.expires_at
        self.rotation_duration = expires_in

        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        return self.access_token

    def generate_custody_auth_header(self, params: AuthParams) -> str:
        """Generate a custody authorization header. Usually invoked from create_new_auth_token.

        Args:
            params (AuthParams): authorization parameters

        Raises:
            Exception: Wallet is required

        Returns:
            str: custody authorization header
        """
        if not self.wallet:
            raise Exception("Wallet not set")
        auth_put_request = AuthPutRequest(params=params)
        payload = auth_put_request.model_dump(by_alias=True, exclude_none=True)
        encoded_payload = canonicaljson.encode_canonical_json(payload)
        signable_message = encode_defunct(primitive=encoded_payload)
        signed_message: SignedMessage = self.wallet.sign_message(signable_message)
        data_hex_array = bytearray(signed_message.signature)
        encoded = base64.b64encode(data_hex_array).decode()
        return f"Bearer eip191:{encoded}"


def get_wallet(
    mnemonic: Optional[str] = None, private_key: Optional[str] = None
) -> Optional[LocalAccount]:
    """Get a wallet from mnemonic or private key

    Args:
        mnemonic (Optional[str]): mnemonic
        private_key (Optional[str]): private key

    Returns:
        Optional[LocalAccount]: wallet
    """
    Account.enable_unaudited_hdwallet_features()

    if mnemonic:
        account: LocalAccount = Account.from_mnemonic(mnemonic)
        return account  # pragma: no cover
    elif private_key:
        account = Account.from_key(private_key)
        return account  # pragma: no cover
    return None


def now_ms() -> int:
    """Get the current time in milliseconds

    Returns:
        int: current time in milliseconds
    """
    return int(time.time() * 1000)
