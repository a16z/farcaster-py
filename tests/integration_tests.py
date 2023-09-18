import os
import time

from dotenv import load_dotenv

from farcaster import Warpcast


def client_from_mnemonic() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    client = Warpcast(mnemonic=MNEMONIC, rotation_duration=200)
    assert client.wallet
    assert client.get_user_by_username("mason").username == "mason"
    assert client.access_token
    assert client.rotation_duration == 200
    print(client.access_token)
    print(client.get_me())


def client_from_pkey() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    assert PKEY, "PKEY env var not set"
    client = Warpcast(private_key=PKEY)
    expiry = (int(time.time()) + (10 * 60)) * 1000
    assert client.wallet
    assert client.get_user_by_username("mason").username == "mason"
    assert client.access_token
    assert client.rotation_duration == 10
    print(client.expires_at)
    print(client.access_token)
    assert client.expires_at == expiry


def client_from_auth() -> Warpcast:
    load_dotenv()
    AUTH = os.getenv("AUTH")
    assert AUTH, "AUTH env var not set"
    client = Warpcast(access_token=AUTH)
    fid = client.get_user_by_username("apitest").fid
    first_cast = client.get_casts(fid=fid).casts[-1]
    me = client.get_me()
    print(me)
    print(first_cast.hash)
    print(client.access_token)
    return client


def test_rotation() -> None:
    load_dotenv()
    PKEY = os.getenv("PKEY")
    client = Warpcast(private_key=PKEY, rotation_duration=1)
    expiry = (int(time.time()) + (60)) * 1000
    while True:
        assert client.wallet
        assert client.get_user_by_username("mason").username == "mason"
        assert client.access_token
        print(client.access_token)
        print(client.expires_at)
        print(expiry)
        print(client.rotation_duration)
        time.sleep(25)


def test_stream_casts() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    client = Warpcast(mnemonic=MNEMONIC)
    print(client.access_token)
    for cast in client.stream_casts():
        if cast:
            print(cast.hash)


def test_stream_users() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    client = Warpcast(mnemonic=MNEMONIC)
    print(client.access_token)
    for user in client.stream_users():
        if user:
            print(user.model_dump())


def test_stream_notifications() -> None:
    load_dotenv()
    MNEMONIC = os.getenv("MNEMONIC")
    assert MNEMONIC, "MNEMONIC env var not set"
    client = Warpcast(mnemonic=MNEMONIC)
    print(client.access_token)
    for notification in client.stream_notifications():
        if notification:
            print(notification.id)
        if notification:
            print(notification.model_dump())


# test_stream_casts()
