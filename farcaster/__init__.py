"""farcaster-py is a Python SDK for the Farcaster Protocol"""

import sys

from .client import MerkleApiClient

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata


def get_version() -> str:
    try:
        return str(importlib_metadata.version(__name__))
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
