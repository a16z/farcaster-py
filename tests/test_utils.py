# import pytest
from typing import List, Union

from pydantic import NoneStr

from farcaster.models import (
    AnyUrl,
    ApiCast,
    ApiUser,
    MentionNotification,
    ReplyNotification,
)
from farcaster.utils.stream_generator import stream_generator


def mock_get_recent_users(cursor: NoneStr, limit: int) -> List[ApiUser]:
    return [
        ApiUser.parse_obj(
            {
                "fid": 1,
                "username": "hello",
                "display_name": "world",
                "registered_at": None,
                "pfp": {
                    "url": AnyUrl(
                        "https://openseauserdata.com/files/20.svg",
                        scheme="https",
                        host="openseauserdata.com",
                        tld="com",
                        host_type="domain",
                        path="/files/20.svg",
                    ),
                    "verified": True,
                },
                "profile": {"bio": {"text": "foo", "mentions": []}},
                "follower_count": 1,
                "following_count": 2,
                "referrer_username": None,
                "viewer_context": {
                    "following": False,
                    "followed_by": False,
                    "can_send_direct_casts": None,
                },
            }
        ),
        ApiUser.parse_obj(
            {
                "fid": 2,
                "username": "hello1",
                "display_name": "world1",
                "registered_at": None,
                "pfp": {
                    "url": AnyUrl(
                        "https://openseauserdata.com/files/20.svg",
                        scheme="https",
                        host="openseauserdata.com",
                        tld="com",
                        host_type="domain",
                        path="/files/20.svg",
                    ),
                    "verified": True,
                },
                "profile": {"bio": {"text": "foo1", "mentions": []}},
                "follower_count": 1,
                "following_count": 2,
                "referrer_username": None,
                "viewer_context": {
                    "following": False,
                    "followed_by": False,
                    "can_send_direct_casts": None,
                },
            }
        ),
        ApiUser.parse_obj(
            {
                "fid": 3,
                "username": "hello2",
                "display_name": "world2",
                "registered_at": None,
                "pfp": {
                    "url": AnyUrl(
                        "https://openseauserdata.com/files/20.svg",
                        scheme="https",
                        host="openseauserdata.com",
                        tld="com",
                        host_type="domain",
                        path="/files/20.svg",
                    ),
                    "verified": True,
                },
                "profile": {"bio": {"text": "foo2", "mentions": []}},
                "follower_count": 1,
                "following_count": 2,
                "referrer_username": None,
                "viewer_context": {
                    "following": False,
                    "followed_by": False,
                    "can_send_direct_casts": None,
                },
            }
        ),
    ]


def mock_get_recent_casts(cursor: NoneStr, limit: int) -> List[ApiCast]:
    return [
        ApiCast.parse_obj(
            {
                "hash": "0x1",
                "thread_hash": "0x2",
                "parent_hash": "0x3",
                "author": {
                    "fid": 1,
                    "username": "1",
                    "display_name": "1",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/1",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="1",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "1", "mentions": []}},
                    "follower_count": 1,
                    "following_count": 1,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "text": "1",
                "timestamp": 1675301079335,
                "mentions": None,
                "attachments": None,
                "ancestors": None,
                "replies": {"count": 0},
                "reactions": {"count": 0},
                "recasts": {"count": 0, "recasters": []},
                "watches": {"count": 0},
                "deleted": None,
                "recast": None,
                "viewer_context": None,
            }
        ),
        ApiCast.parse_obj(
            {
                "hash": "0x2",
                "thread_hash": "0x3",
                "parent_hash": "0x4",
                "author": {
                    "fid": 2,
                    "username": "2",
                    "display_name": "2",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/2",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="2",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "2", "mentions": []}},
                    "follower_count": 2,
                    "following_count": 2,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "text": "2",
                "timestamp": 1675301079335,
                "mentions": None,
                "attachments": None,
                "ancestors": None,
                "replies": {"count": 0},
                "reactions": {"count": 0},
                "recasts": {"count": 0, "recasters": []},
                "watches": {"count": 0},
                "deleted": None,
                "recast": None,
                "viewer_context": None,
            }
        ),
        ApiCast.parse_obj(
            {
                "hash": "0x3",
                "thread_hash": "0x4",
                "parent_hash": "0x5",
                "author": {
                    "fid": 3,
                    "username": "3",
                    "display_name": "3",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/3",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="3",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "3", "mentions": []}},
                    "follower_count": 3,
                    "following_count": 3,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "text": "3",
                "timestamp": 1675301079335,
                "mentions": None,
                "attachments": None,
                "ancestors": None,
                "replies": {"count": 0},
                "reactions": {"count": 0},
                "recasts": {"count": 0, "recasters": []},
                "watches": {"count": 0},
                "deleted": None,
                "recast": None,
                "viewer_context": None,
            }
        ),
    ]


def mock_get_recent_notifications(
    cursor: NoneStr, limit: int
) -> List[Union[MentionNotification, ReplyNotification]]:
    return [
        ReplyNotification.parse_obj(
            {
                "type": "cast-reply",
                "id": "0x1",
                "timestamp": 1674619088162,
                "actor": {
                    "fid": 1,
                    "username": "1",
                    "display_name": "1",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/1",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="1",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "1", "mentions": []}},
                    "follower_count": 1,
                    "following_count": 1,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "content": {"cast": mock_get_recent_casts(None, 1)[0]},
            }
        ),
        MentionNotification.parse_obj(
            {
                "type": "cast-mention",
                "id": "0x2",
                "timestamp": 1674619088162,
                "actor": {
                    "fid": 1,
                    "username": "1",
                    "display_name": "1",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/1",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="1",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "1", "mentions": []}},
                    "follower_count": 1,
                    "following_count": 1,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "content": {"cast": mock_get_recent_casts(None, 1)[0]},
            }
        ),
        ReplyNotification.parse_obj(
            {
                "type": "cast-reply",
                "id": "0x3",
                "timestamp": 1674619088162,
                "actor": {
                    "fid": 1,
                    "username": "1",
                    "display_name": "1",
                    "registered_at": None,
                    "pfp": {
                        "url": AnyUrl(
                            "https://lh3.googleusercontent.com/1",
                            scheme="https",
                            host="lh3.googleusercontent.com",
                            tld="com",
                            host_type="domain",
                            path="1",
                        ),
                        "verified": True,
                    },
                    "profile": {"bio": {"text": "1", "mentions": []}},
                    "follower_count": 1,
                    "following_count": 1,
                    "referrer_username": None,
                    "viewer_context": None,
                },
                "content": {"cast": mock_get_recent_casts(None, 1)[0]},
            }
        ),
    ]


def test_stream_generator_users_pause_after():
    count = 0
    for user in stream_generator(
        mock_get_recent_users, attribute_name="fid", pause_after=-1
    ):
        print(user)
        if count == 3:
            assert user is None
            break
        assert user
        count += 1


def test_stream_generator_users_skip_existing():
    for user in stream_generator(
        mock_get_recent_users, attribute_name="fid", pause_after=-1, skip_existing=True
    ):
        assert user is None
        break


def test_stream_generator_casts_pause_after():
    count = 0
    for cast in stream_generator(
        mock_get_recent_casts, attribute_name="hash", pause_after=-1
    ):
        print(cast)
        if count == 3:
            assert cast is None
            break
        assert cast
        count += 1


def test_stream_generator_casts_skip_existing():
    for cast in stream_generator(
        mock_get_recent_casts, attribute_name="hash", pause_after=-1, skip_existing=True
    ):
        assert cast is None
        break


def test_stream_generator_notifications_pause_after():
    count = 0
    for notification in stream_generator(
        mock_get_recent_notifications, attribute_name="id", pause_after=-1
    ):
        print(notification)
        if count == 3:
            assert notification is None
            break
        assert notification
        count += 1


def test_stream_generator_notifications_skip_existing():
    for cast in stream_generator(
        mock_get_recent_notifications,
        attribute_name="id",
        pause_after=-1,
        skip_existing=True,
    ):
        assert cast is None
        break
