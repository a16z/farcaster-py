from __future__ import annotations

from typing import Any, Dict, Optional

import base64

import canonicaljson
import requests
from eth_account.messages import encode_defunct
from eth_account.signers.local import LocalAccount
from pydantic import PositiveInt

from farcaster.api_models import *
from farcaster.config import *


class MerkleApiClient:
    config: ConfigurationParams
    wallet: LocalAccount | None
    access_token: str | None
    sessions: requests.Session

    def __init__(
        self,
        wallet: LocalAccount | None = None,
        access_token: str | None = None,
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

    def get(
        self,
        path: str,
        params: dict[Any, Any] = {},
        json: dict[Any, Any] = {},
        headers: dict[Any, Any] = {},
    ) -> dict[Any, Any]:
        response: dict[Any, Any] = self.session.get(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])
        return response

    def post(
        self,
        path: str,
        params: dict[Any, Any] = {},
        json: dict[Any, Any] = {},
        headers: dict[Any, Any] = {},
    ) -> dict[Any, Any]:
        response: dict[Any, Any] = self.session.post(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])
        return response

    def put(
        self,
        path: str,
        params: dict[Any, Any] = {},
        json: dict[Any, Any] = {},
        headers: dict[Any, Any] = {},
    ) -> dict[Any, Any]:
        response: dict[Any, Any] = self.session.put(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])
        return response

    def delete(
        self,
        path: str,
        params: dict[Any, Any] = {},
        json: dict[Any, Any] = {},
        headers: dict[Any, Any] = {},
    ) -> dict[Any, Any]:
        response: dict[Any, Any] = self.session.delete(
            self.config.base_path + path, params=params, json=json, headers=headers
        ).json()
        if "errors" in response:
            raise Exception(response["errors"])
        return response

    def get_healthcheck(self) -> bool:
        response = self.session.get("https://api.farcaster.xyz/healthcheck")
        return response.ok

    def get_asset(self, token_id: int) -> AssetGetResponse:
        response = self.get("asset", {"token_id": token_id})
        return AssetGetResponse(**response)

    def get_asset_events(
        self,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> AssetEventsGetResponse:
        response = self.get(
            "asset-events",
            params={"cursor": cursor, "limit": limit},
        )
        return AssetEventsGetResponse(**response)

    def put_auth(self, body: AuthPutRequest) -> AuthPutResponse:
        header = self.generate_custody_auth_header(body)
        response = requests.put(
            "https://api.farcaster.xyz/v2/auth",
            json=body.dict(by_alias=True),
            headers={"Authorization": header},
        ).json()
        return AuthPutResponse(**response)

    def delete_auth(self, body: AuthDeleteRequest) -> StatusResponse:
        response = self.delete(
            "auth",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_cast_reactions(
        self,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CastReactionsGetResponse:
        response = self.get(
            "cast-reactions",
            params={"cursor": cursor, "limit": limit},
        )
        return CastReactionsGetResponse(**response)

    def put_cast_reactions(
        self, body: CastReactionsPutRequest
    ) -> CastReactionsPutResponse:
        response = self.put(
            "cast-reactions",
            json=body.dict(by_alias=True),
        )
        return CastReactionsPutResponse(**response)

    def delete_cast_reactions(self, body: CastReactionsDeleteRequest) -> StatusResponse:
        response = self.delete(
            "cast-reactions",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_cast_likes(
        self,
        cast_hash: str,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CastReactionsGetResponse:
        response = self.get(
            "cast-likes",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastReactionsGetResponse(**response)

    def put_cast_likes(self, body: CastHash) -> CastReactionsPutResponse:
        response = self.put(
            "cast-likes",
            json=body.dict(by_alias=True),
        )
        return CastReactionsPutResponse(**response)

    def delete_cast_likes(self, cast_hash: str, body: CastHash) -> StatusResponse:
        response = self.delete(
            "cast-likes",
            params={"castHash": cast_hash},
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_cast_recasters(
        self,
        cast_hash: str,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CastRecastersGetResponse:
        response = self.get(
            "cast-recasters",
            params={"castHash": cast_hash, "cursor": cursor, "limit": limit},
        )
        return CastRecastersGetResponse(**response)

    def get_cast(
        self,
        hash: str,
    ) -> CastGetResponse:
        response = self.get(
            "cast",
            params={"hash": hash},
        )
        return CastGetResponse(**response)

    def get_all_casts_in_thread(
        self,
        thread_hash: str,
    ) -> CastsGetResponse:
        response = self.get(
            "all-casts-in-thread",
            params={"threadHash": thread_hash},
        )
        return CastsGetResponse(**response)

    def get_casts(
        self,
        fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CastsGetResponse:
        response = self.get(
            "casts",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response)

    def post_casts(self, body: CastsPostRequest) -> Union[None, CastsPostResponse]:
        response = self.post(
            "casts",
            json=body.dict(by_alias=True),
        )
        return CastsPostResponse(**response)

    def delete_casts(self, body: CastHash) -> StatusResponse:
        response = self.delete(
            "casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_collection(self, collection_id: str) -> CollectionGetResponse:
        response = self.get(
            "collection",
            params={"collectionId": collection_id},
        )
        return CollectionGetResponse(**response)

    def get_collection_activity(
        self,
        collection_id: str,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CollectionActivityGetResponse:
        response = self.get(
            "collection-activity",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionActivityGetResponse(**response)

    def get_collection_assets(
        self,
        collection_id: str,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CollectionAssetsGetResponse:
        response = self.get(
            "collection-assets",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionAssetsGetResponse(**response)

    def get_collection_owners(
        self,
        collection_id: str,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> CollectionOwnersGetResponse:
        response = self.get(
            "collection-owners",
            params={"collectionId": collection_id, "cursor": cursor, "limit": limit},
        )
        return CollectionOwnersGetResponse(**response)

    def get_followers(
        self,
        fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> FollowersGetResponse:
        response = self.get(
            "followers",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return FollowersGetResponse(**response)

    def get_following(
        self,
        fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> FollowingGetResponse:
        response = self.get(
            "following",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return FollowingGetResponse(**response)

    def put_follows(self, body: FollowsPutRequest) -> StatusResponse:
        response = self.put(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def delete_follows(self, body: FollowsDeleteRequest) -> StatusResponse:
        response = self.delete(
            "follows",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_me(self) -> MeGetResponse:
        response = self.get(
            "me",
        )
        response_model = MeGetResponse(**response)
        self.config.username = response_model.result.user.username
        return response_model

    def get_mention_and_reply_notifications(
        self,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> MentionAndReplyNotificationsGetResponse:
        response = self.get(
            "mention-and-reply-notifications",
            params={"cursor": cursor, "limit": limit},
        )
        return MentionAndReplyNotificationsGetResponse(**response)

    def put_recasts(self, body: CastHash) -> RecastsPutResponse:
        response = self.put(
            "recasts",
            json=body.dict(by_alias=True),
        )
        return RecastsPutResponse(**response)

    def delete_recasts(self, body: CastHash) -> StatusResponse:
        response = self.delete(
            "recasts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_user(self, fid: str) -> UserGetResponse:
        response = self.get(
            "user",
            params={"fid": fid},
        )
        return UserGetResponse(**response)

    def get_user_by_username(
        self,
        username: str,
    ) -> UserByUsernameGetResponse:
        response = self.get(
            "user-by-username",
            params={"username": username},
        )
        return UserByUsernameGetResponse(**response)

    def get_user_by_verification(
        self,
        address: str,
    ) -> UserByUsernameGetResponse:
        response = self.get(
            "user-by-verification",
            params={"address": address},
        )
        return UserByUsernameGetResponse(**response)

    def get_user_collections(
        self,
        owner_fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> UserCollectionsGetResponse:
        response = self.get(
            "user-collections",
            params={"ownerFid": owner_fid, "cursor": cursor, "limit": limit},
        )
        return UserCollectionsGetResponse(**response)

    def get_verifications(
        self,
        fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> VerificationsGetResponse:
        response = self.get(
            "verifications",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return VerificationsGetResponse(**response)

    def put_watched_casts(self, body: WatchedCastsPutRequest) -> StatusResponse:
        response = self.put(
            "watched-casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def delete_watched_casts(self, body: WatchedCastsDeleteRequest) -> StatusResponse:
        response = self.delete(
            "watched-casts",
            json=body.dict(by_alias=True),
        )
        return StatusResponse(**response)

    def get_recent_users(
        self,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> UsersGetResponse:
        response = self.get(
            "recent-users",
            params={"cursor": cursor, "limit": limit},
        )
        return UsersGetResponse(**response)

    def get_custody_address(
        self,
        fname: str,
        fid: int,
    ) -> CustodyAddressGetResponse:
        response = self.get(
            "custody-address",
            params={"fname": fname, "fid": fid},
        )
        return CustodyAddressGetResponse(**response)

    def get_user_cast_likes(
        self,
        fid: int,
        cursor: str | None = None,
        limit: PositiveInt = 25,
    ) -> UserCastLikesGetResponse:
        response = self.get(
            "user-cast-likes",
            params={"fid": fid, "cursor": cursor, "limit": limit},
        )
        return UserCastLikesGetResponse(**response)

    def get_recent_casts(
        self,
        cursor: str | None = None,
        limit: PositiveInt = 100,
    ) -> CastsGetResponse:
        response = self.get(
            "recent-casts",
            params={"cursor": cursor, "limit": limit},
        )
        return CastsGetResponse(**response)

    def create_new_auth_token(self, params: AuthPutRequest) -> str:
        response = self.put_auth(params)
        self.access_token = response.result.token.secret
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return self.access_token

    def generate_custody_auth_header(self, params: AuthPutRequest) -> str:
        if not self.wallet:
            raise Exception("Wallet not set")

        payload = params.dict(by_alias=True)
        encoded_payload = canonicaljson.encode_canonical_json(payload)
        signable_message = encode_defunct(primitive=encoded_payload)
        signed_message = self.wallet.sign_message(signable_message)
        data_hex_array = bytearray(signed_message.signature)
        encoded = base64.b64encode(data_hex_array).decode()
        return f"Bearer eip191:{encoded}"
