import logging
import os
import time

from dotenv import load_dotenv

from farcaster.client import MerkleApiClient


def fcc_from_mnemonic() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = MerkleApiClient(mnemonic=MNEMONIC)
    assert fcc.wallet
    assert fcc.get_user_by_username("mason").user.username == "mason"
    assert fcc.access_token
    assert fcc.rotation_duration == 10
    assert fcc.expires_at == (int(time.time()) + (10 * 60)) * 1000

    print(fcc.wallet.key.hex())


def fcc_from_pkey() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    assert PKEY, "PKEY env var not set"
    fcc = MerkleApiClient(private_key=PKEY)
    expiry = (int(time.time()) + (10 * 60)) * 1000
    assert fcc.wallet
    assert fcc.get_user_by_username("mason").user.username == "mason"
    assert fcc.access_token
    assert fcc.rotation_duration == 10
    print(fcc.expires_at)
    print(expiry)
    assert fcc.expires_at == expiry


def test_rotation() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    fcc = MerkleApiClient(private_key=PKEY, rotation_duration=1)
    expiry = (int(time.time()) + (60)) * 1000
    while True:
        assert fcc.wallet
        assert fcc.get_user_by_username("mason").user.username == "mason"
        assert fcc.access_token
        print(fcc.access_token)
        print(fcc.expires_at)
        print(expiry)
        print(fcc.rotation_duration)
        time.sleep(25)
