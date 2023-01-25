import logging

import pytest

from farcaster.client import MerkleApiClient
from farcaster.models import CastsPostRequest


@pytest.mark.vcr
def test_get_cast(fcc: MerkleApiClient) -> None:
    """Unit test that gets cast

    Args:
        fcc: fixture

    Returns:
        None
    """
    # get cast
    response = fcc.get_cast(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.cast.author.fid == 3


@pytest.mark.vcr
def test_nonexistent_get_cast(fcc: MerkleApiClient) -> None:
    """Unit test that gets nonexistent cast

    Args:
        fcc: fixture

    Returns:
        None
    """
    # get cast
    with pytest.raises(Exception):
        # Should raise error
        fcc.get_cast(
            "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d861"
        )


@pytest.mark.vcr
def test_get_all_casts_in_thread(fcc: MerkleApiClient) -> None:
    """Unit test that gets all casts in thread

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_all_casts_in_thread(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    print(response)
    assert response.casts[0].author.fid == 3


@pytest.mark.vcr
def test_get_casts(fcc: MerkleApiClient) -> None:
    """Unit test that gets a user's recent casts

    Args:
        fcc: fixture

    Returns:
        None
    """
    response1 = fcc.get_casts(fid=50)
    assert len(response1.casts) == 25
    response2 = fcc.get_casts(fid=50, limit=10)
    assert len(response2.casts) == 10


@pytest.mark.vcr
def test_get_cast_likes(fcc: MerkleApiClient) -> None:
    """Unit test that gets cast likes

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_cast_likes(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.likes[0].reactor.fid == 43


@pytest.mark.vcr
def test_get_cast_recasters(fcc: MerkleApiClient) -> None:
    """Unit test that gets cast recasters

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_cast_recasters(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.users[0].username == "adrienne"


@pytest.mark.vcr
def test_get_recent_casts(fcc: MerkleApiClient) -> None:
    """Unit test that gets all recent casts

    Args:
        fcc: fixture

    Returns:
        None
    """
    response1 = fcc.get_recent_casts()
    assert len(response1.casts) == 100
    response2 = fcc.get_recent_casts(limit=50)
    assert len(response2.casts) == 50


@pytest.mark.vcr
@pytest.mark.dependency()
def test_follow_user(fcc: MerkleApiClient) -> None:
    """Unit test that follows user

    Args:
        fcc: fixture

    Returns:
        None
    """
    fid = fcc.get_user_by_username(username="mmm").user.fid
    status = fcc.follow_user(fid=fid)
    assert status.success


@pytest.mark.vcr
@pytest.mark.dependency(depends=["test_follow_user"])
def test_unfollow_user(fcc: MerkleApiClient) -> None:
    """Unit test that unfollows user

    Args:
        fcc: fixture

    Returns:
        None
    """
    fid = fcc.get_user_by_username(username="mmm").user.fid
    status = fcc.unfollow_user(fid=fid)
    assert status.success


@pytest.mark.vcr
def test_get_followers(fcc: MerkleApiClient) -> None:
    """Unit test that gets followers

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_followers(fid=50)
    assert len(response.users) == 25
    response = fcc.get_followers(fid=50, limit=100)
    assert len(response.users) == 100


@pytest.mark.vcr
def test_get_following(fcc: MerkleApiClient) -> None:
    """Unit test that gets who a user is following

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_following(fid=50)
    assert len(response.users) == 25
    response = fcc.get_following(fid=50, limit=100)
    assert len(response.users) == 100


@pytest.mark.vcr
def test_get_user(fcc: MerkleApiClient) -> None:
    """Unit test that gets user

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_user(fid=50)
    assert response.user.username == "mason"


@pytest.mark.vcr
def test_get_user_by_username(fcc: MerkleApiClient) -> None:
    """Unit test that gets user by username

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_user_by_username(username="mason")
    assert response.user.username == "mason"
    assert response.user.fid == 50


@pytest.mark.vcr
def test_get_user_cast_likes(fcc: MerkleApiClient) -> None:
    """Unit test that gets user cast likes

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_user_cast_likes(fid=50)
    assert len(response.likes) == 25
    response = fcc.get_user_cast_likes(fid=50, limit=100)
    assert len(response.likes) == 100


@pytest.mark.vcr
def test_get_custody_address(fcc: MerkleApiClient) -> None:
    """Unit test that gets custody address

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_custody_address(username="mason")
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    response = fcc.get_custody_address(fid=50)
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    with pytest.raises(Exception):
        # Must provide either fname or fid
        fcc.get_custody_address()


@pytest.mark.vcr
def test_get_me(fcc: MerkleApiClient) -> None:
    """Unit test that gets user

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_me()
    assert response.user.username == "apitest"


@pytest.mark.vcr
def test_get_recent_users(fcc: MerkleApiClient) -> None:
    """Unit test that gets recent users

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_recent_users()
    assert len(response.users) == 25
    assert response.users[0].fid > response.users[1].fid


@pytest.mark.vcr
def test_get_verifications(fcc: MerkleApiClient) -> None:
    """Unit test that gets verifications

    Args:
        fcc: fixture

    Returns:
        None
    """
    response = fcc.get_verifications(fid=50)
    logging.debug(response)
    assert response.verifications[0].fid == 50


@pytest.mark.vcr
def test_get_user_by_verification(fcc: MerkleApiClient) -> None:
    """Unit test that gets user by verification

    Args:
        fcc: fixture

    Returns:
        None
    """
    with pytest.raises(Exception):
        response = fcc.get_user_by_verification(
            address="0x000000000877cb2a6cbce87a34f0d2fd7cb4ad3e"
        )
    response = fcc.get_user_by_verification(
        address="0xDC40CbF86727093c52582405703e5b97D5C64B66"
    )
    assert response.user.username == "mason"


class TestRW:
    """Read/write tests"""

    cast_hash = ""

    @pytest.mark.vcr
    @pytest.mark.dependency()
    def test_post_cast(self, fcc: MerkleApiClient) -> None:
        """Unit test that posts cast

        Args:
            fcc: fixture

        Returns:
            None
        """
        cast_body = CastsPostRequest(
            text="Hello world from our WIP Farcaster Python SDK!"
        )
        response = fcc.post_cast(cast_body)
        logging.debug(response.cast.dict())
        assert response.cast
        self.__class__.cast_hash = response.cast.hash
        assert isinstance(self.__class__.cast_hash, str)

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_like_cast(self, fcc: MerkleApiClient) -> None:
        """Unit test that puts cast likes

        Args:
            fcc: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        response = fcc.like_cast(self.__class__.cast_hash)
        assert response.like.cast_hash

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_like_cast"])
    def test_delete_cast_likes(self, fcc: MerkleApiClient) -> None:
        """Unit test that deletes cast likes

        Args:
            fcc: fixture

        Returns:
            None
        """
        logging.debug(self.__class__.cast_hash)
        response = fcc.delete_cast_likes(self.__class__.cast_hash)
        assert response.success

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_recast(self, fcc: MerkleApiClient) -> None:
        """Unit test that recasts cast

        Args:
            fcc: fixture

        Returns:
            None
        """
        response = fcc.recast(self.__class__.cast_hash)
        assert response.cast_hash

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_recast"])
    def test_delete_recast(self, fcc: MerkleApiClient) -> None:
        """Unit test that deletes recast

        Args:
            fcc: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        logging.debug(self.__class__.cast_hash)
        response = fcc.delete_recast(self.__class__.cast_hash)
        assert response.success

    @pytest.mark.vcr
    @pytest.mark.dependency(depends=["TestRW::test_post_cast"])
    def test_delete_cast(self, fcc: MerkleApiClient) -> None:
        """Unit test that deletes cast

        Args:
            fcc: fixture

        Returns:
            None
        """
        assert self.__class__.cast_hash
        logging.debug(self.__class__.cast_hash)
        response = fcc.delete_cast(self.__class__.cast_hash)
        assert response.success
