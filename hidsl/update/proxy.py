"""Multiprocessing proxies."""

from datetime import datetime
from multiprocessing.managers import NamespaceProxy
from typing import Union


__all__ = ['get_success', 'get_pending', 'to_json', 'to_csv']


def get_tasks(namespace: NamespaceProxy) -> Union[bool, None]:
    """Yields the tasks."""

    try:
        yield namespace.keyring
    except AttributeError:
        yield None

    try:
        yield namespace.sysupgrade
    except AttributeError:
        yield None

    try:
        yield namespace.cleanup
    except AttributeError:
        yield None


def get_success(namespace: NamespaceProxy) -> bool:
    """Determines whether the system update succeeded."""

    return all(task is None or task for task in get_tasks(namespace))


def get_pending(namespace: NamespaceProxy) -> Union[bool, None]:
    """Determines whether the system check is still pending."""

    try:
        started = namespace.started
    except AttributeError:
        started = None

    try:
        finished = namespace.finished
    except AttributeError:
        finished = None

    return started is not None and finished is None


def get_duration(namespace: NamespaceProxy) -> Union[datetime, None]:
    """Calculates the duration of the upgrade process."""

    try:
        started = namespace.started
    except AttributeError:
        return False

    try:
        finished = namespace.finished
    except AttributeError:
        return False

    return finished - started


def to_json(namespace: NamespaceProxy) -> dict:
    """Returns a JSON-ish dict."""

    try:
        started = namespace.started
    except AttributeError:
        started = None

    try:
        finished = namespace.finished
    except AttributeError:
        finished = None

    duration = get_duration(namespace)

    try:
        keyring = namespace.keyring
    except AttributeError:
        keyring = None

    try:
        sysupgrade = namespace.sysupgrade
    except AttributeError:
        sysupgrade = None

    try:
        cleanup = namespace.cleanup
    except AttributeError:
        cleanup = None

    return {
        'started': started.isoformat() if started else None,
        'finished': finished.isoformat() if finished else None,
        'duration': str(duration) if duration else None,
        'keyring': keyring,
        'sysupgrade': sysupgrade,
        'cleanup': cleanup,
        'success': get_success(namespace)
    }


def to_csv(namespace: NamespaceProxy, *, sep: str = ',') -> str:
    """Returns a tuple for CSV representation."""

    return sep.join(str(value) for value in to_json(namespace).values())
