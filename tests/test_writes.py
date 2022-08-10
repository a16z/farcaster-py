import os

from dotenv import load_dotenv
from eth_account.account import Account
from eth_account.signers.local import LocalAccount

from farcaster.client import FarcasterClient

load_dotenv()

ETH_ACCOUNT_SIGNATURE: LocalAccount = Account.from_key(os.environ.get("RINKEBY_PKEY"))

fcc = FarcasterClient(
    os.getenv("RINKEBY_NETWORK_ADDR"), signature_account=ETH_ACCOUNT_SIGNATURE
)


# def test_register():
#     response_hash = fcc.register("xxx")
#     assert response_hash


# def test_transfer():
#     response_hash = fcc.transfer("xxx")
#     assert False


# def test_publish_cast():
#     response = fcc.publish_cast("Hello world! This cast was published from my Python SDK")
#     assert False
