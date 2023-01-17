import logging

import pytest

from farcaster.client import MerkleApiClient


@pytest.mark.vcr
def test_put_auth(fcc: MerkleApiClient) -> None:
    """
    Unit test that puts auth
    :param fcc: fixture
    :return: None
    """
    # response = fcc.put_auth()
    # assert response
    pass


@pytest.mark.vcr
def test_delete_auth(fcc: MerkleApiClient) -> None:
    """
    Unit test that deletes auth
    :param fcc: fixture
    :return: None
    """
    # response = fcc.delete_auth()
    # assert response
    pass
