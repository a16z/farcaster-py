from typing import Any, Dict, Optional

import base64
import logging
import time

import canonicaljson
import requests
from eth_account.account import Account
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from pydantic import NoneStr, PositiveInt

from farcaster.config import *
from farcaster.models import *


class MerkleApiClient:
    """The MerkleApiClient class is a wrapper around the Farcaster API.
    It also provides a number of helpful methods and utilities for interacting with the protocol.
    Pydantic models are used under the hood to validate the data returned from the API.
    """

    config: ConfigurationParams
    wallet: Optional[LocalAccount]
    access_token: NoneStr
    sessions: requests.Session

    def __init__(
        self,
        mnemonic: NoneStr = None,
        private_key: NoneStr = None,
        access_token: NoneStr = None,
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
            raise Exception(response["errors"])
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
            raise Exception(response["errors"])
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
            raise Exception(response["errors"])
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
            raise Exception(response["errors"])
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
        response = self.session.get("https://api.farcaster.xyz/healthcheck")
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
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> EventsResult:
        """Get events for a given asset

        Args:
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): events to receive, defaults
                to 25

        Returns:
            EventsResult: Returns the EventsResult model
        """
        response = self._get(
            "asset-events",
            params={"cursor": cursor, "limit": limit},
        )
        return AssetEventsGetResponse(**response).result

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
            "https://api.farcaster.xyz/v2/auth",
            json=body.dict(by_alias=True),
            headers={"Authorization": header},
        ).json()
        return AuthPutResponse(**response).result

    def delete_auth(self, timestamp: PositiveInt) -> StatusResponse:
        """Delete an access token

        Args:
            timestamp (PositiveInt): The timestamp of the access
                token to delete

        Returns:
            StatusResponse: Status of the deletion
        """
        body = AuthDeleteRequest(params=Timestamp(timestamp=timestamp))
        response = self._delete(
            "auth",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_cast_likes(
        self,
        cast_hash: str,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> ReactionsResult:
        """Get the likes for a given cast

        Args:
            cast_hash (str): cast hash
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            ReactionsResult: ReactionsResult model of likes
        """
        response = self._get(
            "cast-likes",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastReactionsGetResponse(**response).result

    def like_cast(self, body: CastHash) -> ReactionsResult:
        """Like a given cast

        Args:
            body (CastHash): hash of the cast to like

        Returns:
            ReactionsResult: Result of liking the cast
        """
        response = self._put(
            "cast-likes",
            json=body.dict(by_alias=True),
        )
        return CastReactionsPutResponse(**response).result

    def delete_cast_likes(self, cast_hash: str, body: CastHash) -> StatusResponse:
        """Remove a like from a cast

        Args:
            cast_hash (str): hash of the cast to unlike
            body (CastHash): hash of the cast to unlike

        Returns:
            StatusResponse: Status of the deletion
        """
        response = self._delete(
            "cast-likes",
            params={"castHash": cast_hash},
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_cast_recasters(
        self,
        cast_hash: str,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        """Get the recasters for a given cast

        Args:
            cast_hash (str): cast hash
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            UsersResult: Model containing the recasters
        """
        response = self._get(
            "cast-recasters",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastRecastersGetResponse(**response).result

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
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> CastsResult:
        """Get the casts for a given fid of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            CastsResult: Model containing the casts
        """
        response = self._get(
            "casts",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response).result

    def post_cast(self, body: CastsPostRequest) -> CastContent:
        """Post a cast to Farcaster

        Args:
            body (CastsPostRequest): The cast data structure

        Returns:
            CastContent: The result of posting the cast
        """
        response = self._post(
            "casts",
            json=body.dict(by_alias=True),
        )
        return CastsPostResponse(**response).result

    def delete_cast(self, cast_hash: str) -> StatusResponse:
        """Delete a cast

        Args:
            cast_hash (str): the hash of the cast to delete

        Returns:
            StatusResponse: Status of the deletion
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._delete(
            "casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_collection(self, collection_id: str) -> CollectionResult:
        """Get a specific collection

        Args:
            collection_id (str): OpenSea collection ID

        Returns:
            CollectionResult: collection
        """
        response = self._get(
            "collection",
            params={"collectionId": collection_id},
        )
        return CollectionGetResponse(**response).result

    def get_collection_activity(
        self,
        collection_id: str,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> EventsResult:
        """Get collection activity

        Args:
            collection_id (str): OpenSea collection ID
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            EventsResult: Model containing events
        """
        response = self._get(
            "collection-activity",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionActivityGetResponse(**response).result

    def get_collection_assets(
        self,
        collection_id: str,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> AssetsResult:
        """Get assets in an OpenSea collection

        Args:
            collection_id (str): OpenSea collection ID
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            AssetsResult: model containing assets
        """
        response = self._get(
            "collection-assets",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionAssetsGetResponse(**response).result

    def get_collection_owners(
        self,
        collection_id: str,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        """Get the owners of an OpenSea collection

        Args:
            collection_id (str): OpenSea collection ID
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            UsersResult: model containing users
        """
        response = self._get(
            "collection-owners",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionOwnersGetResponse(**response).result

    def get_followers(
        self,
        fid: int,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        """Get the followers of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            UsersResult: model containing users
        """
        response = self._get(
            "followers",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return FollowersGetResponse(**response).result

    def get_following(
        self,
        fid: int,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        """Get the users a user is following

        Args:
            fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            UsersResult: model containing users
        """
        response = self._get(
            "following",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return FollowingGetResponse(**response).result

    def follow_user(self, fid: PositiveInt) -> StatusResponse:
        """Follow a user

        Args:
            fid (PositiveInt): Farcaster ID of the user to follow

        Returns:
            StatusResponse: Status of the follow
        """
        body = FollowsPutRequest(target_fid=fid)
        response = self._put(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def unfollow_user(self, fid: PositiveInt) -> StatusResponse:
        """Unfollow a user

        Args:
            fid (PositiveInt): Farcaster ID of the user to unfollow

        Returns:
            StatusResponse: Status of the unfollow
        """
        body = FollowsDeleteRequest(target_fid=fid)
        response = self._delete(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_me(self) -> UserResult:
        """Get the current user

        Returns:
            UserResult: model containing the current user
        """
        response = self._get(
            "me",
        )
        response_model = MeGetResponse(**response).result
        self.config.username = response_model.user.username
        return response_model

    def get_mention_and_reply_notifications(
        self,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> NotificationsResult:
        """Get mention and reply notifications

        Args:
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            NotificationsResult: model containing notifications
        """
        response = self._get(
            "mention-and-reply-notifications",
            params={"cursor": cursor, "limit": limit},
        )
        return MentionAndReplyNotificationsGetResponse(**response).result

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
            json=body.dict(by_alias=True),
        )
        return RecastsPutResponse(**response).result

    def delete_recast(self, cast_hash: str) -> StatusResponse:
        """Delete a recast

        Args:
            cast_hash (str): the cast hash

        Returns:
            StatusResponse: Status of the recast deletion
        """
        body = CastHash(cast_hash=cast_hash)
        response = self._delete(
            "recasts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_user(self, fid: int) -> UserResult:
        """Get a user

        Args:
            fid (int): Farcaster ID of the user

        Returns:
            UserResult: model containing the user
        """
        response = self._get(
            "user",
            params={"fid": fid},
        )
        return UserGetResponse(**response).result

    def get_user_by_username(
        self,
        username: str,
    ) -> UserResult:
        """Get a user by username

        Args:
            username (str): username of the user

        Returns:
            UserResult: model containing the user
        """
        response = self._get(
            "user-by-username",
            params={"username": username},
        )
        return UserByUsernameGetResponse(**response).result

    def get_user_by_verification(
        self,
        address: str,
    ) -> UserResult:
        """Get a user by verification address

        Args:
            address (str): address of the user

        Returns:
            UserResult: model containing the user
        """
        response = self._get(
            "user-by-verification",
            params={"address": address},
        )
        return UserByUsernameGetResponse(**response).result

    def get_user_collections(
        self,
        owner_fid: int,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> CollectionsResult:
        """Get the collections of a user

        Args:
            owner_fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            CollectionsResult: model containing collections
        """
        response = self._get(
            "user-collections",
            params={"ownerFid": owner_fid, "cursor": cursor, "limit": limit},
        )
        return UserCollectionsGetResponse(**response).result

    def get_verifications(
        self,
        fid: int,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> VerificationsResult:
        """Get the verifications of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            VerificationsResult: model containing verifications
        """
        response = self._get(
            "verifications",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return VerificationsGetResponse(**response).result

    def get_recent_users(
        self,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        """Get recent users

        Args:
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            UsersResult: model containing users
        """
        response = self._get(
            "recent-users",
            params={"cursor": cursor, "limit": limit},
        )
        return UsersGetResponse(**response).result

    def get_custody_address(
        self,
        username: NoneStr = None,
        fid: Optional[int] = None,
    ) -> CustodyAddress:
        """Get the custody address of a user

        Args:
            username (NoneStr, optional): username of a user, defaults
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
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> Likes:
        """Get the likes of a user

        Args:
            fid (int): Farcaster ID of the user
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 25

        Returns:
            Likes: model containing likes
        """
        response = self._get(
            "user-cast-likes",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return UserCastLikesGetResponse(**response).result

    def get_recent_casts(
        self,
        cursor: NoneStr = None,
        limit: PositiveInt = 100,
    ) -> CastsResult:
        """Get all recent casts

        Args:
            cursor (NoneStr, optional): cursor, defaults to None
            limit (PositiveInt, optional): limit, defaults to 100

        Returns:
            CastsResult: model containing casts
        """
        response = self._get(
            "recent-casts",
            params={"cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response).result

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
        payload = auth_put_request.dict(by_alias=True)
        encoded_payload = canonicaljson.encode_canonical_json(payload)
        signable_message = encode_defunct(primitive=encoded_payload)
        signed_message = self.wallet.sign_message(signable_message)
        data_hex_array = bytearray(signed_message.signature)
        encoded = base64.b64encode(data_hex_array).decode()
        return f"Bearer eip191:{encoded}"


def get_wallet(mnemonic: NoneStr, private_key: NoneStr) -> Optional[LocalAccount]:
    """Get a wallet from mnemonic or private key

    Args:
        mnemonic (NoneStr): mnemonic
        private_key (NoneStr): private key

    Returns:
        Optional[LocalAccount]: wallet
    """
    Account.enable_unaudited_hdwallet_features()

    if mnemonic:
        account: LocalAccount = Account.from_mnemonic(mnemonic)
        return account
    elif private_key:
        account = Account.from_key(private_key)
        return account
    return None


def now_ms() -> int:
    """Get the current time in milliseconds

    Returns:
        int: current time in milliseconds
    """
    return int(time.time() * 1000)
