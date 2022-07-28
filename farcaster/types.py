from typing import Any, List, Optional

import humps
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        alias_generator = humps.camelize
        exclude_none = True


class CastData(BaseModel):
    text: str
    reply_parent_merkle_root: Optional[str] = None


class CastBody(BaseModel):
    type: str
    published_at: int
    sequence: int
    username: str
    address: str
    data: CastData
    prev_merkle_root: str


class Reactions(BaseModel):
    count: int
    type: str
    self: bool


class Recasts(BaseModel):
    count: int
    self: bool


class Watches(BaseModel):
    count: int
    self: bool


class ReplyParentUsername(BaseModel):
    address: str
    username: str


class Attachments(BaseModel):
    opengraph: List[Any]


class Meta(BaseModel):
    display_name: str
    avatar: str
    is_verified_avatar: bool
    num_reply_children: int
    reactions: Reactions
    recasts: Recasts
    watches: Watches
    reply_parent_username: Optional[ReplyParentUsername]
    attachments: Optional[Attachments]


class Cast(BaseModel):
    body: CastBody
    merkle_root: str
    signature: str
    meta: Meta


class HostBody(BaseModel):
    address_activity_url: str
    avatar_url: str
    display_name: str
    proof_url: str
    timestamp: int
    version: int


class HostDirectory(BaseModel):
    body: HostBody
    merkle_root: str
    signature: str
