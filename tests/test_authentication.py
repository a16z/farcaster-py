from typing import Any

import time

import pytest
import requests

from farcaster.client import Warpcast, now_ms
from farcaster.models import *


# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"result": {"success": "true"}}


class MockResponsePut:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {
            "result": {
                "token": {
                    "secret": "MK-ABC123...",
                    "expiresAt": 1610000000000,
                }
            }
        }


@pytest.mark.vcr
def test_auth_params(client: Warpcast) -> None:
    """Unit test that tests auth params model

    Args:
        client: fixture

    Returns:
        None
    """
    now = int(time.time())
    obj = {"timestamp": now * 1000, "expiresAt": int(now + 600) * 1000}
    ap = AuthParams(**obj)
    assert ap.dict(by_alias=True) == obj


def test_now_ms() -> None:
    """Unit test that tests now_ms function"""
    assert abs(now_ms() - int(time.time() * 1000)) < 1000


@pytest.mark.vcr
def test_create_new_auth_token_no_wallet(client: Warpcast) -> None:
    """Unit test that puts auth

    Args:
        client: fixture

    Returns:
        None
    """
    with pytest.raises(Exception, match="^Wallet not set$"):
        client.create_new_auth_token(expires_in=10)


@pytest.mark.vcr
def test_delete_auth(monkeypatch: Any, client: Warpcast) -> None:
    """Unit test that deletes auth

    Args:
        monkeypatch: fixture
        client: fixture

    Returns:
        None
    """

    def mock_delete(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse()

    monkeypatch.setattr(requests.Session, "delete", mock_delete)

    response = client.delete_auth()
    assert response.success


@pytest.mark.vcr
def test_put_auth(monkeypatch: Any, client: Warpcast) -> None:
    """Unit test that test put auth

    Args:
        monkeypatch: fixture
        client: fixture

    Returns:
        None
    """

    def mock_put(*args: Any, **kwargs: Any) -> MockResponsePut:
        return MockResponsePut()

    def mock_header(*args: Any, **kwargs: Any) -> str:
        return "eip191:V5Opo6K5M6JECBNurxHDtbts3Uqh/QpisEwm0ZSPqQdXrnTBvBZDZSME3HPeq/1pGP7ISwKJocGeWZESMxxxxxx"

    monkeypatch.setattr(requests, "put", mock_put)
    monkeypatch.setattr(Warpcast, "generate_custody_auth_header", mock_header)

    now = int(time.time())
    obj = {"timestamp": now * 1000, "expiresAt": int(now + 600) * 1000}
    ap = AuthParams(**obj)
    response = client.put_auth(auth_params=ap)
    assert response.token.secret
