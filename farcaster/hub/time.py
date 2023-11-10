from typing import Optional

import time
from datetime import datetime

FARCASTER_EPOCH = 1609459200000  # January 1, 2021 UTC


def get_farcaster_time() -> Optional[int]:
    return to_farcaster_time(time.time_ns() // 1_000_000)


def to_farcaster_time(time: int) -> Optional[int]:
    if time < FARCASTER_EPOCH:
        # time must be after Farcaster epoch (01/01/2022)
        return None

    seconds_since_epoch = (time - FARCASTER_EPOCH) // 1000

    if seconds_since_epoch > (2**32) - 1:
        # time too far in future
        return None

    return seconds_since_epoch


def from_farcaster_time(time: int) -> int:
    return (time * 1000) + FARCASTER_EPOCH


def datetime_from_farcaster_time(time: int) -> datetime:
    return datetime.fromtimestamp(from_farcaster_time(time) / 1_000)
