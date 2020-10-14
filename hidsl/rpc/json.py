"""Functions to JSON-isfy dicts."""

from datetime import datetime
from typing import Iterable, Tuple, Union


__all__ = ['to_json']


JSONValue = Union[bool, dict, float, int, list, str]
JSONTuple = Tuple[str, JSONValue]


def get_duration(dictionary: dict) -> Union[datetime, None]:
    """Calculates the duration of the upgrade process."""

    if (start := dictionary.get('start')) is None:
        return None

    if (end := dictionary.get('end')) is None:
        return None

    return end - start


def json_values(dictionary: dict) -> Iterable[JSONTuple]:
    """Yields key / value pairs for a JSON-ish dict."""

    for key, value in dictionary.items():
        if isinstance(value, datetime):
            value = value.isoformat()

        yield (key, value)

    if (duration := get_duration(dictionary)) is not None:
        duration = duration.isoformat()

    yield ('duration', duration)


def to_json(dictionary: dict) -> dict:
    """Returns a JSON-ish dict."""

    return dict(json_values(dictionary))
