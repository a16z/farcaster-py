import logging

import pytest

from farcaster.client import MerkleApiClient


def test_mention_reply_notifications(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets a user's recent notifications. Has to be the user who owns the access token
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_mention_and_reply_notifications(limit=10)
    assert len(response.notifications) == 10


def test_get_user_collections(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets a user's collections
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_user_collections(owner_fid=50)
    assert len(response.collections) > 1


def test_get_collection_owners(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets a collection's owners
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_collection_owners(collection_id="proof-of-merge")
    assert len(response.users) > 1


def test_get_healthcheck(fcc: MerkleApiClient) -> None:
    """
    Unit test that gets healthcheck
    :param fcc: fixture
    :return: None
    """
    response = fcc.get_healthcheck()
    assert response
