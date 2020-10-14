"""Functions to access the multiprocessing namespace."""

from datetime import datetime
from multiprocessing.managers import DictProxy
from typing import Iterable, Tuple, Union


__all__ = ['get_pending', 'to_json']


JSONValue = Union[bool, dict, float, int, list, str]
JSONTuple = Tuple[str, JSONValue]


def get_pending(dict_proxy: DictProxy) -> Union[bool, None]:
    """Determines whether the system check is still pending."""

    if dict_proxy.get('start') is None:
        return None

    if dict_proxy.get('end') is None:
        return True

    return False


def get_duration(dict_proxy: DictProxy) -> Union[datetime, None]:
    """Calculates the duration of the upgrade process."""

    if (start := dict_proxy.get('start')) is None:
        return None

    if (end := dict_proxy.get('end')) is None:
        return None

    return end - start


def json_values(dict_proxy: DictProxy) -> Iterable[JSONTuple]:
    """Yields key / value pairs for a JSON-ish dict."""

    for key, value in dict_proxy.items():
        if isinstance(value, datetime):
            value = value.isoformat()

        yield (key, value)

    if (duration := get_duration(dict_proxy)) is not None:
        duration = duration.isoformat()

    yield ('duration', duration)


def to_json(dict_proxy: DictProxy) -> dict:
    """Returns a JSON-ish dict."""

    return dict(json_values(dict_proxy))
