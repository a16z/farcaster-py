import os

import pytest
from dotenv import load_dotenv

from farcaster.client import MerkleApiClient


@pytest.fixture(scope="session", autouse=True)
def fcc() -> MerkleApiClient:
    load_dotenv()
    access_token = os.getenv("AUTH")
    assert access_token, "AUTH env var not set"
    return MerkleApiClient(access_token=access_token)
