import pytest

from farcaster.client import MerkleApiClient, get_wallet


def test_get_base_path(fcc: MerkleApiClient) -> None:
    """Unit test that gets a user's recent notifications. Has to be the user who owns the access token

    Args:
        fcc: fixture

    Returns:
        None
    """
    assert fcc.get_base_path()


def test_get_base_options(fcc: MerkleApiClient) -> None:
    """Unit test that gets a user's recent notifications. Has to be the user who owns the access token

    Args:
        fcc: fixture

    Returns:
        None
    """
    assert fcc.get_base_options() is None


def test_get_wallet() -> None:
    """Unit test that tests initialization of a wallet

    Returns:
        None
    """
    assert get_wallet() is None
    with pytest.raises(Exception):
        get_wallet(mnemonic="test")
    with pytest.raises(Exception):
        get_wallet(private_key="test")
