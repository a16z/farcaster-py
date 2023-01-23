import logging
import time

import pytest

from farcaster.client import MerkleApiClient
from farcaster.models import *


@pytest.mark.vcr
def test_auth_params(fcc: MerkleApiClient) -> None:
    """Unit test that tests auth params model

    Args:
        fcc: fixture

    Returns:
        None
    """
    # response = fcc.put_auth()
    # assert response
    now = int(time.time())
    obj = {"timestamp": now * 1000, "expiresAt": int(now + 600) * 1000}
    ap = AuthParams(**obj)
    assert ap.dict(by_alias=True) == obj


@pytest.mark.vcr
def test_create_new_auth_token(fcc: MerkleApiClient) -> None:
    """Unit test that puts auth

    Args:
        fcc: fixture

    Returns:
        None
    """
    with pytest.raises(Exception, match="^Wallet not set$"):
        fcc.create_new_auth_token(expires_in=10)


@pytest.mark.vcr
def test_delete_auth(fcc: MerkleApiClient) -> None:
    """Unit test that deletes auth

    Args:
        fcc: fixture

    Returns:
        None
    """
    # response = fcc.delete_auth()
    # assert response
    pass
