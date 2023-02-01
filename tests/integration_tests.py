import os
import time

from dotenv import load_dotenv

from farcaster.client import MerkleApiClient


def fcc_from_mnemonic() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = MerkleApiClient(mnemonic=MNEMONIC, rotation_duration=200)
    assert fcc.wallet
    assert fcc.get_user_by_username("mason").user.username == "mason"
    assert fcc.access_token
    assert fcc.rotation_duration == 200
    print(fcc.access_token)
    print(fcc.get_me())


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
    print(fcc.access_token)
    assert fcc.expires_at == expiry


def fcc_from_auth() -> MerkleApiClient:
    load_dotenv()
    AUTH = os.getenv("AUTH")
    assert AUTH, "AUTH env var not set"
    fcc = MerkleApiClient(access_token=AUTH)
    fid = fcc.get_user_by_username("apitest").user.fid
    first_cast = fcc.get_casts(fid=fid).casts[-1]
    me = fcc.get_me()
    print(me)
    print(first_cast.hash)
    print(fcc.access_token)
    return fcc


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


def test_stream_casts() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = MerkleApiClient(mnemonic=MNEMONIC)
    print(fcc.access_token)
    for cast in fcc.stream_casts():
        print(cast.hash)


def test_stream_users() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = MerkleApiClient(mnemonic=MNEMONIC)
    print(fcc.access_token)
    for user in fcc.stream_users():
        print(user.username)


def test_stream_notifications() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = MerkleApiClient(mnemonic=MNEMONIC)
    print(fcc.access_token)
    for notification in fcc.stream_notifications():
        print(notification.id)
        print(notification.content.dict())
