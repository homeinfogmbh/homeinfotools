"""Multiprocessing proxies."""

from datetime import datetime
from multiprocessing.managers import DictProxy


__all__ = ['UpdateJobProxy']


class UpdateJobProxy:
    """Represents the update state of a system."""

    def __init__(self, dict_proxy: DictProxy):
        super().__setattr__('dict_proxy', dict_proxy)

    def __getattr__(self, attr):
        return self.dict_proxy.get(attr)

    def __setattr__(self, attr, value):
        self.dict_proxy[attr] = value

    def __enter__(self):
        self.started = datetime.now()   # pylint: disable=W0201
        return self

    def __exit__(self, *_):
        self.finished = datetime.now()  # pylint: disable=W0201

    @property
    def tasks(self):
        """Yields the tasks."""
        yield self.keyring
        yield self.sysupgrade
        yield self.cleanup

    @property
    def success(self):
        """Determines whether the system update succeeded."""
        return all(task is None or task for task in self.tasks)

    @property
    def pending(self):
        """Determines whether the system check is still pending."""
        return self.started is not None and self.finished is None

    @property
    def duration(self):
        """Calculates the duration of the upgrade process."""
        if self.started is None or self.finished is None:
            return None

        return self.finished - self.started

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {
            'started': self.started.isoformat() if self.started else None,
            'finished': self.finished.isoformat() if self.finished else None,
            'duration': str(dur) if (dur := self.duration) else dur,
            'keyring': self.keyring,
            'sysupgrade': self.sysupgrade,
            'cleanup': self.cleanup,
            'success': self.success
        }

    def to_csv(self, *, sep: str = ',') -> str:
        """Returns a tuple for CSV representation."""
        return sep.join(str(value) for value in self.to_json().values())
