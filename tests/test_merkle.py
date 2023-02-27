import pytest

from farcaster.client import Warpcast


@pytest.mark.vcr
def test_mention_reply_notifications(client: Warpcast) -> None:
    """Unit test that gets a user's recent notifications. Has to be the user who owns the access token

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_mention_and_reply_notifications(limit=150)
    assert len(response.notifications) > 2


@pytest.mark.vcr
def test_get_user_collections(client: Warpcast) -> None:
    """Unit test that gets a user's collections

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_user_collections(owner_fid=50)
    assert len(response.collections) > 1


@pytest.mark.vcr
def test_get_collection_owners(client: Warpcast) -> None:
    """Unit test that gets a collection's owners

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_collection_owners(collection_id="proof-of-merge", limit=10000)
    assert len(response.users) > 101


@pytest.mark.vcr
def test_get_healthcheck(client: Warpcast) -> None:
    """Unit test that gets healthcheck

    Args:
        client: fixture

    Returns:
        None
    """
    response = client.get_healthcheck()
    assert response
