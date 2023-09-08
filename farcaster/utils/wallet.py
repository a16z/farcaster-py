from typing import Optional

from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from pydantic import NoneStr


def get_wallet(
    mnemonic: NoneStr = None, private_key: NoneStr = None
) -> Optional[LocalAccount]:
    """Get a wallet from mnemonic or private key

    Args:
        mnemonic (NoneStr): mnemonic
        private_key (NoneStr): private key

    Returns:
        Optional[LocalAccount]: wallet
    """
    Account.enable_unaudited_hdwallet_features()

    if mnemonic:
        account: LocalAccount = Account.from_mnemonic(mnemonic)
        return account  # pragma: no cover
    elif private_key:
        account = Account.from_key(private_key)
        return account  # pragma: no cover
    return None
