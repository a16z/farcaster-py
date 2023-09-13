# import pytest
from typing import List, Optional, Union

from farcaster.models import ApiCast, ApiUser, MentionNotification, ReplyNotification
from farcaster.utils.stream_generator import (
    BoundedSet,
    ExponentialCounter,
    stream_generator,
)


def mock_get_recent_users(cursor: Optional[str], limit: int) -> List[ApiUser]:
    return [
        ApiUser.model_validate(
            {
                "fid": 1,
                "username": "hello",
                "display_name": "world",
                "registered_at": None,
                "pfp": {
                    "url": "https://openseauserdata.com/files/20.svg",
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
        ApiUser.model_validate(
            {
                "fid": 2,
                "username": "hello1",
                "display_name": "world1",
                "registered_at": None,
                "pfp": {
                    "url": "https://openseauserdata.com/files/20.svg",
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
        ApiUser.model_validate(
            {
                "fid": 3,
                "username": "hello2",
                "display_name": "world2",
                "registered_at": None,
                "pfp": {
                    "url": "https://openseauserdata.com/files/20.svg",
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


def mock_get_recent_casts(cursor: Optional[str], limit: int) -> List[ApiCast]:
    return [
        ApiCast.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/1",
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
                "embeds": None,
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
        ApiCast.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/2",
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
                "embeds": None,
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
        ApiCast.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/3",
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
                "embeds": None,
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
    cursor: Optional[str], limit: int
) -> List[Union[MentionNotification, ReplyNotification]]:
    return [
        ReplyNotification.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/1",
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
        MentionNotification.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/1",
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
        ReplyNotification.model_validate(
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
                        "url": "https://lh3.googleusercontent.com/1",
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


def test_bounded_set():
    b_set = BoundedSet(3)
    b_set.add(1)
    assert 1 in b_set
    b_set.add(2)
    assert 2 in b_set
    b_set.add(3)
    assert 3 in b_set
    b_set.add(4)
    assert 1 not in b_set


def test_exponential_counter():
    counter = ExponentialCounter(5)
    count1 = counter.counter()
    assert count1 > 0 and count1 <= 1.5
    count2 = counter.counter()
    assert count2 > count1


def test_exponential_counter_reset():
    counter = ExponentialCounter(5)
    [counter.counter() for _ in range(5)]
    assert counter.counter() > 4
    counter.reset()
    assert counter.counter() < 2
