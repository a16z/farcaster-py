import logging

import pytest

from farcaster.client import MerkleApiClient


@pytest.mark.vcr
def test_get_cast(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets cast
    :param fcc: fixture
    :return: None
    """
    # get cast
    response = fcc.get_cast(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.cast.author.fid == 3


@pytest.mark.vcr
def test_nonexistent_get_cast(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets nonexistent cast
    :param fcc: fixture
    :return: None
    """
    # get cast
    with pytest.raises(Exception):
        # Should raise error
        response = fcc.get_cast(
            "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d861"
        )


@pytest.mark.vcr
def test_get_all_casts_in_thread(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets all casts in thread
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_all_casts_in_thread(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    print(response)
    assert response.casts[0].author.fid == 3


@pytest.mark.vcr
def test_get_casts(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets a user's recent casts
    :param fcc: fixture
    :return: None
    """
    response1 = fcc.get_casts(fid=50)
    assert len(response1.casts) == 25
    response2 = fcc.get_casts(fid=50, limit=10)
    assert len(response2.casts) == 10


@pytest.mark.vcr
def test_post_cast(fcc: MerkleApiClient) -> None:
    """
    Unit test that posts cast
    :param fcc: fixture
    :return: None
    """
    # cast_body = CastsPostRequest(text="Hello world from our WIP Farcaster Python SDK!")
    # # post cast
    # response = fcc.post_cast(cast_body)
    # if response:
    #     print(response.cast.hash)
    # else:
    #     raise Exception("Failed to post cast")
    pass


@pytest.mark.vcr
def test_delete_cast(fcc: MerkleApiClient) -> None:
    """
    Unit test that deletes cast
    :param fcc: fixture
    :return: None
    """
    # cast_body = CastsPostRequest(text="Hello world from our WIP Farcaster Python SDK!")
    # # post cast
    # response = fcc.delete_cast(cast_body)
    # if response:
    #     print(response)
    pass


@pytest.mark.vcr
def test_get_cast_likes(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets cast likes
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_cast_likes(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.likes[0].reactor.fid == 43


@pytest.mark.vcr
def test_put_cast_likes(fcc: MerkleApiClient) -> None:
    """
    Unit test that puts cast likes
    :param fcc: fixture
    :return: None
    """
    # cast_body = CastsPostRequest(text="Hello world from our WIP Farcaster Python SDK!")
    # # post cast
    # response = fcc.put_cast_likes(cast_body)
    # if response:
    pass


@pytest.mark.vcr
def test_delete_cast_likes(fcc: MerkleApiClient) -> None:
    """
    Unit test that deletes cast likes
    :param fcc: fixture
    :return: None
    """
    # cast_body = CastsPostRequest(text="Hello world from our WIP Farcaster Python SDK!")
    # # post cast
    # response = fcc.delete_cast_likes(cast_body)
    # if response:
    pass


@pytest.mark.vcr
def test_get_cast_recasters(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets cast recasters
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_cast_recasters(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
    assert response.users[0].username == "adrienne"


@pytest.mark.vcr
def test_recast_cast(fcc: MerkleApiClient) -> None:
    """
    Unit test that recasts cast
    :param fcc: fixture
    :return: None
    """
    pass


@pytest.mark.vcr
def test_delete_recast(fcc: MerkleApiClient) -> None:
    """
    Unit test that deletes recast
    :param fcc: fixture
    :return: None
    """
    pass


@pytest.mark.vcr
def test_get_recent_casts(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets all recent casts
    :param fcc: fixture
    :return: None
    """
    response1 = fcc.get_recent_casts()
    assert len(response1.casts) == 100
    response2 = fcc.get_recent_casts(limit=50)
    assert len(response2.casts) == 50


@pytest.mark.vcr
def test_follow_user(fcc: MerkleApiClient) -> None:
    """
    Unit test that follows user
    :param fcc: fixture
    :return: None
    """
    pass


@pytest.mark.vcr
def test_unfollow_user(fcc: MerkleApiClient) -> None:
    """
    Unit test that unfollows user
    :param fcc: fixture
    :return: None
    """
    pass


@pytest.mark.vcr
def test_get_followers(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets followers
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_followers(fid=50)
    assert len(response.users) == 25
    response = fcc.get_followers(fid=50, limit=100)
    assert len(response.users) == 100


@pytest.mark.vcr
def test_get_following(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets who a user is following
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_following(fid=50)
    assert len(response.users) == 25
    response = fcc.get_following(fid=50, limit=100)
    assert len(response.users) == 100


@pytest.mark.vcr
def test_get_user(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets user
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_user(fid=50)
    assert response.user.username == "mason"


@pytest.mark.vcr
def test_get_user_by_username(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets user by username
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_user_by_username(username="mason")
    assert response.user.username == "mason"
    assert response.user.fid == 50


@pytest.mark.vcr
def test_get_user_cast_likes(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets user cast likes
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_user_cast_likes(fid=50)
    assert len(response.likes) == 25
    response = fcc.get_user_cast_likes(fid=50, limit=100)
    assert len(response.likes) == 100


@pytest.mark.vcr
def test_get_custody_address(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets custody address
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_custody_address(fname="mason")
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    response = fcc.get_custody_address(fid=50)
    assert response.custody_address == "0x044991055877cb2a6cbce87a34f0d2fd7cb4ad3e"
    with pytest.raises(Exception):
        # Must provide either fname or fid
        fcc.get_custody_address()


@pytest.mark.vcr
def test_get_me(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets user
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_me()
    assert response.user.username == "mason"


@pytest.mark.vcr
def test_get_recent_users(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets recent users
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_recent_users()
    assert len(response.users) == 25
    assert response.users[0].fid > response.users[1].fid


def test_get_verifications(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets verifications
    :param fcc: fixture
    :return: None
    """
    # response = fcc.get_verifications(fid=50)
    # logging.debug(response)
    # assert response.verifications[0].fid == 50
    pass


def test_get_user_by_verification(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets user by verification
    :param fcc: fixture
    :return: None
    """
    # with pytest.raises(Exception):
    #     response = fcc.get_user_by_verification(
    #         address="0x000000000877cb2a6cbce87a34f0d2fd7cb4ad3e"
    #     )
    # response = fcc.get_user_by_verification(
    #     address="0xDC40CbF86727093c52582405703e5b97D5C64B66"
    # )
    # assert response.user.username == "mason"
    pass
