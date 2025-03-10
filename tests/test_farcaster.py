from typing import Any, List

import logging

import pytest

from farcaster import Warpcast, models


@pytest.mark.vcr
def test_get_conversation_participants(client: Warpcast) -> None:
    """Unit test that gets a conversation and the participants in it

    Args:
        client: fixture

    Returns:
        None

    """

    # This will only work for my account as it's a group conversation on my account
    response = client.get_conversation_participants(
        "5d741f42a6016e1f0bb1eb9ef15a049cdfdffd72c486aa5f72a150da34ade054"
    )

    assert len(response) > 0


@pytest.mark.vcr
def test_get_non_existent_conversation(client: Warpcast) -> None:
    """Unit test that gets a nonexistent conversation

    Args:
        client: fixture

    Returns:
        None

    """

    with pytest.raises(Exception):
        # Should raise error
        client.get_conversation_participants("nonexistent")


@pytest.mark.vcr
def test_get_cast(client: Warpcast) -> None:
    """Unit test that gets cast

    Args:
        client: fixture

    Returns:
        None
    """
    # get cast
    response = client.get_cast(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.cast.author.fid == 3


@pytest.mark.vcr
def test_nonexistent_get_cast(client: Warpcast) -> None:
    """Unit test that gets nonexistent cast

    Args:
        client: fixture

    Returns:
        None
    """
    # get cast
    with pytest.raises(Exception):
        # Should raise error
        client.get_cast(
            "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d861"
        )


@pytest.mark.vcr
def test_get_all_casts_in_thread(client: Warpcast) -> None:
    """Unit test that gets all casts in thread

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_all_casts_in_thread(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    print(response)
    assert response.casts[0].author.fid == 3


@pytest.mark.vcr
def test_get_casts(client: Warpcast) -> None:
    """Unit test that gets a user's recent casts

    Args:
        client: fixture

    Returns:
        None
    """
    response1 = client.get_casts(fid=50)
    assert len(response1.casts) == 25
    response2 = client.get_casts(fid=3, limit=150)
    assert len(response2.casts) == 150


@pytest.mark.vcr
def test_get_cast_likes(client: Warpcast) -> None:
    """Unit test that gets cast likes

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_cast_likes(
        cast_hash="0x5fbc51755100112aaecbc0b5f5fbdc07bc4aa311afb10bfe2436f5fa6824cfd1",
        limit=150,
    )
    assert len(response.likes) > 50


@pytest.mark.vcr
def test_get_cast_recasters(client: Warpcast) -> None:
    """Unit test that gets cast recasters

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_cast_recasters(
        cast_hash="0xdbf9f2f37b806f2d613a8b20ea96597956a9c02e3a49abeb75c84e5a1f9bd5f9",
        limit=100,
    )
    assert len(response.users) > 20


@pytest.mark.vcr
def test_get_recent_casts(client: Warpcast) -> None:
    """Unit test that gets all recent casts

    Args:
        client: fixture

    Returns:
        None
    """
    response1 = client.get_recent_casts()
    assert len(response1.casts) == 100
    response2 = client.get_recent_casts(limit=150)
    assert len(response2.casts) == 150


@pytest.mark.vcr
@pytest.mark.dependency()
def test_follow_user(client: Warpcast) -> None:
    """Unit test that follows user

    Args:
        client: fixture

    Returns:
        None
    """
    fid = client.get_user_by_username(username="mmm").fid
    status = client.follow_user(fid=fid)
    assert status.success


@pytest.mark.vcr
@pytest.mark.dependency(depends=["test_follow_user"])
def test_unfollow_user(client: Warpcast) -> None:
    """Unit test that unfollows user

    Args:
        client: fixture

    Returns:
        None
    """
    fid = client.get_user_by_username(username="mmm").fid
    status = client.unfollow_user(fid=fid)
    assert status.success


@pytest.mark.vcr
def test_get_followers(client: Warpcast) -> None:
    """Unit test that gets followers

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_followers(fid=50)
    assert len(response.users) == 25
    response = client.get_followers(fid=50, limit=150)
    assert len(response.users) == 150


@pytest.mark.vcr
def test_get_following(client: Warpcast) -> None:
    """Unit test that gets who a user is following

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_following(fid=50)
    assert len(response.users) == 25
    response = client.get_following(fid=3, limit=1000)
    assert len(response.users) == 1000


@pytest.mark.vcr
def test_get_all_following(client: Warpcast) -> None:
    """Unit test that gets everyone who a user is following

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_all_following(fid=50)
    assert len(response.users) >= 196


@pytest.mark.vcr
def test_get_all_followers(client: Warpcast) -> None:
    """Unit test that gets everyone who follows a user
    Args:
        client: fixture
    Returns:
        None
    """
    response = client.get_all_followers(fid=50)
    assert len(response.users) >= 200


@pytest.mark.vcr
def test_get_user(client: Warpcast) -> None:
    """Unit test that gets user

    Args:
        client: fixture

    Returns:
        None
    """
    user = client.get_user(fid=50)
    assert user.username == "mason"


@pytest.mark.vcr
def test_get_user_by_username(client: Warpcast) -> None:
    """Unit test that gets user by username

    Args:
        client: fixture

    Returns:
        None
    """
    user = client.get_user_by_username(username="mason")
    assert user.username == "mason"
    assert user.fid == 50


@pytest.mark.vcr
def test_get_user_cast_likes(client: Warpcast) -> None:
    """Unit test that gets user cast likes

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_user_cast_likes(fid=50)
    assert len(response.likes[0].cast_hash) == 42
    assert len(response.likes) == 25
    response = client.get_user_cast_likes(fid=50, limit=200)
    assert len(response.likes) == 200


@pytest.mark.vcr
def test_get_custody_address(client: Warpcast) -> None:
    """Unit test that gets custody address

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_custody_address(username="mason")
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    response = client.get_custody_address(fid=50)
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    with pytest.raises(Exception):
        # Must provide either fname or fid
        client.get_custody_address()


@pytest.mark.vcr
def test_get_me(client: Warpcast) -> None:
    """Unit test that gets user

    Args:
        client: fixture

    Returns:
        None
    """
    user = client.get_me()
    assert user.username == "apitest"


@pytest.mark.vcr
def test_get_recent_users(client: Warpcast) -> None:
    """Unit test that gets recent users

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_recent_users(limit=200)
    assert len(response.users) == 200
    assert response.users[0].fid > response.users[101].fid


@pytest.mark.vcr
def test_get_verifications(client: Warpcast) -> None:
    """Unit test that gets verifications

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_verifications(fid=50)
    logging.debug(response)
    assert response.verifications[0].fid == 50


@pytest.mark.vcr
def test_get_user_by_verification(client: Warpcast) -> None:
    """Unit test that gets user by verification

    Args:
        client: fixture

    Returns:
        None
    """
    with pytest.raises(Exception):
        user = client.get_user_by_verification(
            address="0x000000000877cb2a6cbce87a34f0d2fd7cb4ad3e"
        )
    user = client.get_user_by_verification(
        address="0xDC40CbF86727093c52582405703e5b97D5C64B66"
    )
    assert user.username == "mason"


@pytest.mark.vcr
def test_stream_casts(client: Warpcast) -> None:
    """Unit test that tests streaming casts

    Args:
        client: fixture

    Returns:
        None
    """
    casts: List[models.ApiCast] = []
    for cast in client.stream_casts(pause_after=-1):
        if cast is None:
            break
        casts.append(cast)

    assert len(casts) == 50


@pytest.mark.vcr
def test_stream_casts_skip_existing(client: Warpcast) -> None:
    """Unit test that tests streaming casts

    Args:
        client: fixture

    Returns:
        None
    """
    for cast in client.stream_casts(pause_after=-1, skip_existing=True):
        assert cast is None
        break


@pytest.mark.vcr
def test_stream_users(client: Warpcast) -> None:
    """Unit test that tests streaming users

    Args:
        client: fixture

    Returns:
        None
    """
    users: List[models.ApiUser] = []
    for user in client.stream_users(pause_after=-1):
        if user is None:
            break
        users.append(user)

    assert len(users) == 20


@pytest.mark.vcr
def test_stream_users_skip_existing(client: Warpcast) -> None:
    """Unit test that tests streaming users

    Args:
        client: fixture

    Returns:
        None
    """
    for user in client.stream_users(pause_after=-1, skip_existing=True):
        assert user is None
        break


@pytest.mark.vcr
def test_stream_notifications(client: Warpcast) -> None:
    """Unit test that tests streaming notifications

    Args:
        client: fixture

    Returns:
        None
    """
    notifications: List[Any] = []
    for notification in client.stream_notifications(pause_after=-1):
        if notification is None:
            break
        notifications.append(notification)

    assert len(notifications) == 1


@pytest.mark.vcr
def test_stream_notifications_skip_existing(client: Warpcast) -> None:
    """Unit test that tests streaming notifications

    Args:
        client: fixture

    Returns:
        None
    """
    for notification in client.stream_notifications(pause_after=-1, skip_existing=True):
        assert notification is None
        break


class TestRW:
    """Read/write tests"""

    cast_hash = ""

    @pytest.mark.vcr
    @pytest.mark.dependency()
    def test_post_cast(self, client: Warpcast) -> None:
        """Unit test that posts cast

        Args:
            client: fixture

        Returns:
            None
        """
        response = client.post_cast(
            text="Hello world from our WIP Farcaster Python SDK!"
        )
        logging.debug(response.cast.model_dump())
        assert response.cast
        self.__class__.cast_hash = response.cast.hash
        assert isinstance(self.__class__.cast_hash, str)

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_like_cast(self, client: Warpcast) -> None:
        """Unit test that puts cast likes

        Args:
            client: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        response = client.like_cast(self.__class__.cast_hash)
        assert response.like.cast_hash

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_like_cast"])
    def test_delete_cast_likes(self, client: Warpcast) -> None:
        """Unit test that deletes cast likes

        Args:
            client: fixture

        Returns:
            None
        """
        logging.debug(self.__class__.cast_hash)
        response = client.delete_cast_likes(self.__class__.cast_hash)
        assert response.success

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_recast(self, client: Warpcast) -> None:
        """Unit test that recasts cast

        Args:
            client: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        response = client.recast(self.__class__.cast_hash)
        assert response.cast_hash

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_recast"])
    def test_delete_recast(self, client: Warpcast) -> None:
        """Unit test that deletes recast

        Args:
            client: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        logging.debug(self.__class__.cast_hash)
        response = client.delete_recast(self.__class__.cast_hash)
        assert response.success

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_delete_cast(self, client: Warpcast) -> None:
        """Unit test that deletes cast

        Args:
            client: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        logging.debug(self.__class__.cast_hash)
        response = client.delete_cast(self.__class__.cast_hash)
        assert response.success
