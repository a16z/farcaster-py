import os

import pytest
from dotenv import load_dotenv

from farcaster.client import Warpcast


@pytest.fixture(scope="session", autouse=True)
def fcc() -> Warpcast:
    load_dotenv()
    access_token = os.getenv("AUTH")
    assert access_token, "AUTH env var not set"
    return Warpcast(access_token=access_token)


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["authorization", "DUMMY"]}
