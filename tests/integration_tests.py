import os
import time

from dotenv import load_dotenv

from farcaster.client import Warpcast


def fcc_from_mnemonic() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = Warpcast(mnemonic=MNEMONIC, rotation_duration=200)
    assert fcc.wallet
    assert fcc.get_user_by_username("mason").username == "mason"
    assert fcc.access_token
    assert fcc.rotation_duration == 200
    print(fcc.access_token)
    print(fcc.get_me())


def fcc_from_pkey() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    assert PKEY, "PKEY env var not set"
    fcc = Warpcast(private_key=PKEY)
    expiry = (int(time.time()) + (10 * 60)) * 1000
    assert fcc.wallet
    assert fcc.get_user_by_username("mason").username == "mason"
    assert fcc.access_token
    assert fcc.rotation_duration == 10
    print(fcc.expires_at)
    print(fcc.access_token)
    assert fcc.expires_at == expiry


def fcc_from_auth() -> Warpcast:
    load_dotenv()
    AUTH = os.getenv("AUTH")
    assert AUTH, "AUTH env var not set"
    fcc = Warpcast(access_token=AUTH)
    fid = fcc.get_user_by_username("apitest").fid
    first_cast = fcc.get_casts(fid=fid).casts[-1]
    me = fcc.get_me()
    print(me)
    print(first_cast.hash)
    print(fcc.access_token)
    return fcc


def test_rotation() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    fcc = Warpcast(private_key=PKEY, rotation_duration=1)
    expiry = (int(time.time()) + (60)) * 1000
    while True:
        assert fcc.wallet
        assert fcc.get_user_by_username("mason").username == "mason"
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
    fcc = Warpcast(mnemonic=MNEMONIC)
    print(fcc.access_token)
    # fid = 50
    # all_following = fcc.get_all_following(fid=fid)
    # print(len(all_following.users))
    for cast in fcc.stream_casts():
        if cast:
            print(cast.hash)


def test_stream_users() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = Warpcast(mnemonic=MNEMONIC)
    print(fcc.access_token)
    for user in fcc.stream_users():
        if user:
            print(user.dict())


def test_stream_notifications() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    fcc = Warpcast(mnemonic=MNEMONIC)
    print(fcc.access_token)
    for notification in fcc.stream_notifications():
        if notification:
            print(notification.id)
        if notification:
            print(notification.dict())


# test_stream_casts()
