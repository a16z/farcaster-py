import os

import pytest
from dotenv import load_dotenv

from farcaster import Warpcast


@pytest.fixture(scope="session", autouse=True)
def client() -> Warpcast:
    load_dotenv()
    # access_token = os.getenv("AUTH")
    # assert access_token, "AUTH env var not set"
    NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY")
    assert NEYNAR_API_KEY, "PKEY env var not set"
    return Warpcast(neynar_api_key=NEYNAR_API_KEY)
    # return Warpcast(access_token=access_token)


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["authorization", "DUMMY"]}
