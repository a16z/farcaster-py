import os

import pytest
from dotenv import load_dotenv

from farcaster import Hub, Warpcast


@pytest.fixture(scope="session", autouse=True)
def client() -> Warpcast:
    load_dotenv()
    access_token = os.getenv("AUTH")
    assert access_token, "AUTH env var not set"
    return Warpcast(access_token=access_token)


@pytest.fixture(scope="session", autouse=True)
def hub() -> Hub:
    load_dotenv()
    mnemonic = os.getenv("MNEMONIC")
    farcaster_hub = os.getenv("FARCASTER_HUB")
    use_ssl = os.getenv("FARCASTER_USE_SSL") == "true"
    assert mnemonic, "MNEMONIC env var not set"
    assert farcaster_hub, "FARCASTER_HUB env var not set"
    return Hub(mnemonic=mnemonic, hub_address=farcaster_hub, use_ssl=use_ssl)


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["authorization", "DUMMY"]}
