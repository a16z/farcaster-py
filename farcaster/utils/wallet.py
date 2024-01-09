from typing import Optional

from eth_account.account import Account
from eth_account.signers.local import LocalAccount


def get_wallet(
    mnemonic: Optional[str] = None, private_key: Optional[str] = None
) -> Optional[LocalAccount]:
    """Get a wallet from mnemonic or private key
    Args:
        mnemonic (Optional[str]): mnemonic
        private_key (Optional[str]): private key
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
