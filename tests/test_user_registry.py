import os

from dotenv import load_dotenv
from eth_account.account import Account
from eth_account.signers.local import LocalAccount

# from farcaster.client import FarcasterClient

# load_dotenv()

# ETH_ACCOUNT_SIGNATURE: LocalAccount = Account.from_key(os.environ.get("RINKEBY_PKEY"))

# fcc = FarcasterClient(
#     os.getenv("RINKEBY_NETWORK_ADDR", "rinkeby"),
#     signature_account=ETH_ACCOUNT_SIGNATURE,
# )


# def test_lookup_by_username():
#     user = fcc.lookup_by_username("dwr")
#     assert user
#     assert user.username == "dwr"


# def test_get_all_users():
#     users = fcc.get_all_users()
#     assert users
#     assert len(users) > 0


# def test_get_all_usernames():
#     usernames = fcc.get_all_usernames()
#     assert usernames
#     assert len(usernames) > 0


# def test_lookup_by_address():
#     user = fcc.lookup_by_address("0xC6C0b79d0034A9A44c01c7695EaE26c9A7d23e40")
#     assert user
#     assert user.username == "dwr"
