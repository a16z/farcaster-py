from typing import Any, Callable, Iterator, List, Optional, Union

import logging
import random
import time
from collections import OrderedDict

from pydantic import NoneStr, PositiveInt

from farcaster.models import ApiCast, ApiUser, MentionNotification, ReplyNotification

Streamable = Union[
    List[Union[MentionNotification, ReplyNotification]],
    List[ApiUser],
    List[ApiCast],
]


def stream_generator(
    function: Callable[
        [NoneStr, int],
        Streamable,
    ],
    *,
    attribute_name: str = "hash",
    pause_after: Optional[int] = None,
    skip_existing: bool = False,
    max_counter: PositiveInt = 16,
    limit: int = 50,
    cursor: NoneStr = None,
) -> Iterator[Any]:
    """Yield new items from ``function`` as they become available.

    Args:
        function: A function that returns a list of items.
        attribute_name: The name of the attribute to use to determine if an item is new
        pause_after: The number of times to call ``function`` without finding a new item
        skip_existing: If ``True``, skip items that existed before the stream was created
        max_counter: The maximum number of seconds to wait between calls to ``function``
        limit: The maximum number of items to request from ``function`` at a time
        cursor: The cursor to use when calling ``function``

    Yields:
        Iterator[Yieldable]: A generator that yields new items from ``function`` as they become available.
    """
    before_attribute = None
    exponential_counter = ExponentialCounter(max_counter=max_counter)
    seen_attributes = BoundedSet(301)
    without_before_counter = 0
    responses_without_new = 0
    while True:
        found = False
        newest_attribute = None
        dynamic_limit = limit
        if before_attribute is None:
            dynamic_limit -= without_before_counter
            without_before_counter = (without_before_counter + 1) % int(limit / 2)
        logging.debug("Limit: ", dynamic_limit)
        for item in reversed(list(function(cursor, dynamic_limit))):
            attribute = getattr(item, attribute_name)
            if attribute in seen_attributes:
                continue
            found = True
            seen_attributes.add(attribute)
            newest_attribute = attribute
            if not skip_existing:
                yield item
        before_attribute = newest_attribute
        skip_existing = False
        if pause_after is not None and pause_after < 0:
            yield None
        elif found:
            exponential_counter.reset()
            responses_without_new = 0
        else:
            responses_without_new += 1
            if pause_after is not None:
                if responses_without_new > pause_after:
                    exponential_counter.reset()
                    responses_without_new = 0
                    yield None
            else:
                time.sleep(exponential_counter.counter())


class BoundedSet:
    """A set with a maximum size that evicts the oldest items when necessary.
    This class does not implement the complete set interface.
    """

    _set: OrderedDict[Any, Any]

    def __contains__(self, item: Any) -> bool:
        """Test if the :class:`.BoundedSet` contains item."""
        self._access(item)
        return item in self._set

    def __init__(self, max_items: int):
        """Initialize a :class:`.BoundedSet` instance."""
        self.max_items = max_items
        self._set = OrderedDict()

    def _access(self, item: Any) -> None:
        if item in self._set:
            self._set.move_to_end(item)

    def add(self, item: Any) -> None:
        """Add an item to the set discarding the oldest item if necessary."""
        self._access(item)
        self._set[item] = None
        if len(self._set) > self.max_items:
            self._set.popitem(last=False)


class ExponentialCounter:
    """A class to provide an exponential counter with jitter."""

    def __init__(self, max_counter: int):
        """Initialize an :class:`.ExponentialCounter` instance.
        :param max_counter: The maximum base value.
            .. note::
                The computed value may be 3.125% higher due to jitter.
        """
        self._base = 1
        self._max = max_counter

    def counter(self) -> Union[int, float]:
        """Increment the counter and return the current value with jitter."""
        max_jitter = self._base / 16.0
        value = self._base + random.random() * max_jitter - max_jitter / 2
        self._base = min(self._base * 2, self._max)
        logging.debug(f"Sleeping for {value} seconds")
        return value

    def reset(self):
        """Reset the counter to 1."""
        self._base = 1
