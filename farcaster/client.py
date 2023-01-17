from typing import Any, Dict, Optional

import base64
import logging

import canonicaljson
import requests
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from pydantic import NoneStr, PositiveInt

from farcaster.config import *
from farcaster.models import *


class MerkleApiClient:
    config: ConfigurationParams
    wallet: Optional[LocalAccount]
    access_token: NoneStr
    sessions: requests.Session

    def __init__(
        self,
        wallet: Optional[LocalAccount] = None,
        access_token: NoneStr = None,
        **data: Any,
    ):
        self.config = ConfigurationParams(**data)
        self.wallet = wallet
        self.access_token = access_token
        self.session = requests.Session()
        if self.access_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )

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
        logging.debug(f"DELETE {path} {params} {json} {headers}")
        response: Dict[Any, Any] = self.session.delete(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])
        return response

    def get_healthcheck(self) -> bool:
        """Check if API is up and running

        :return: Status of the API
        :rtype: bool
        """
        response = self.session.get("https://api.farcaster.xyz/healthcheck")
        return response.ok

    def get_asset(self, token_id: int) -> AssetResult:
        """Get asset information

        :param token_id: token ID
        :type token_id: int
        :return: token information
        :rtype: AssetResult
        """
        response = self._get("asset", {"token_id": token_id})
        return AssetGetResponse(**response).result

    def get_asset_events(
        self,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> EventsResult:
        """Get events for a given asset

        :param cursor: cursor, defaults to None
        :type cursor: NoneStr, optional
        :param limit: events to receive, defaults to 25
        :type limit: PositiveInt, optional
        :return: Returns the EventsResult model
        :rtype: EventsResult
        """
        response = self._get(
            "asset-events",
            params={"cursor": cursor, "limit": limit},
        )
        return AssetEventsGetResponse(**response).result

    def put_auth(self, auth_params: AuthParams) -> TokenResult:
        """Generate a custody bearer token and use it to generate an access token

        :param auth_params: _description_
        :type auth_params: AuthParams
        :return: _description_
        :rtype: TokenResult
        """
        header = self.generate_custody_auth_header(auth_params)
        body = AuthPutRequest(params=auth_params)
        response = requests.put(
            "https://api.farcaster.xyz/v2/auth",
            json=body.dict(by_alias=True),
            headers={"Authorization": header},
        ).json()
        return AuthPutResponse(**response).result

    def delete_auth(self, body: AuthDeleteRequest) -> StatusResponse:
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
        response = self._get(
            "cast-likes",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastReactionsGetResponse(**response).result

    def put_cast_likes(self, body: CastHash) -> ReactionsResult:
        response = self._put(
            "cast-likes",
            json=body.dict(by_alias=True),
        )
        return CastReactionsPutResponse(**response).result

    def delete_cast_likes(self, cast_hash: str, body: CastHash) -> StatusResponse:
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
        response = self._get(
            "cast-recasters",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastRecastersGetResponse(**response).result

    def get_cast(
        self,
        hash: str,
    ) -> CastContent:
        response = self._get(
            "cast",
            params={"hash": hash},
        )
        return CastGetResponse(**response).result

    def get_all_casts_in_thread(
        self,
        thread_hash: str,
    ) -> CastsResult:
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
        response = self._get(
            "casts",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response).result

    def post_cast(self, body: CastsPostRequest) -> Union[None, CastContent]:
        response = self._post(
            "casts",
            json=body.dict(by_alias=True),
        )
        return CastsPostResponse(**response).result

    def delete_casts(self, body: CastHash) -> StatusResponse:
        response = self._delete(
            "casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_collection(self, collection_id: str) -> CollectionResult:
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
        response = self._get(
            "following",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return FollowingGetResponse(**response).result

    def put_follows(self, body: FollowsPutRequest) -> StatusResponse:
        response = self._put(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def delete_follows(self, body: FollowsDeleteRequest) -> StatusResponse:
        response = self._delete(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_me(self) -> UserResult:
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
        response = self._get(
            "mention-and-reply-notifications",
            params={"cursor": cursor, "limit": limit},
        )
        return MentionAndReplyNotificationsGetResponse(**response).result

    def put_recasts(self, body: CastHash) -> CastHash:
        response = self._put(
            "recasts",
            json=body.dict(by_alias=True),
        )
        return RecastsPutResponse(**response).result

    def delete_recasts(self, body: CastHash) -> StatusResponse:
        response = self._delete(
            "recasts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_user(self, fid: int) -> UserResult:
        response = self._get(
            "user",
            params={"fid": fid},
        )
        return UserGetResponse(**response).result

    def get_user_by_username(
        self,
        username: str,
    ) -> UserResult:
        response = self._get(
            "user-by-username",
            params={"username": username},
        )
        return UserByUsernameGetResponse(**response).result

    def get_user_by_verification(
        self,
        address: str,
    ) -> UserResult:
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
        response = self._get(
            "verifications",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return VerificationsGetResponse(**response).result

    def put_watched_casts(self, body: WatchedCastsPutRequest) -> StatusResponse:
        response = self._put(
            "watched-casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def delete_watched_casts(self, body: WatchedCastsDeleteRequest) -> StatusResponse:
        response = self._delete(
            "watched-casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_recent_users(
        self,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> UsersResult:
        response = self._get(
            "recent-users",
            params={"cursor": cursor, "limit": limit},
        )
        return UsersGetResponse(**response).result

    def get_custody_address(
        self,
        fname: NoneStr = None,
        fid: Optional[int] = None,
    ) -> CustodyAddress:
        assert fname or fid, "fname or fid must be provided"
        response = self._get(
            "custody-address",
            params={"fname": fname, "fid": fid},
        )
        return CustodyAddressGetResponse(**response).result

    def get_user_cast_likes(
        self,
        fid: int,
        cursor: NoneStr = None,
        limit: PositiveInt = 25,
    ) -> Likes:
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
        response = self._get(
            "recent-casts",
            params={"cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response).result

    def create_new_auth_token(self, params: AuthParams) -> str:
        response = self.put_auth(params)
        self.access_token = response.token.secret
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return self.access_token

    def generate_custody_auth_header(self, params: AuthParams) -> str:
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
