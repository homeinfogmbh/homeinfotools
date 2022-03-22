"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime
from multiprocessing import Queue

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker']


class BaseWorker:   # pylint: disable=R0903
    """Stored args and manager to process systems."""

    __slots__ = ('args', 'systems')

    def __init__(self, args: Namespace, systems: Queue[int]):
        """Sets the command line arguments."""
        self.args = args
        self.systems = systems

    def __call__(self, system: int) -> tuple[int, dict]:
        """Runs the worker on the given system."""
        result = {'start': (start := datetime.now()).isoformat()}

        try:
            self.run(system, result)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')
            result['success'] = False
        else:
            result['success'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)
        return (system, result)

    def run(self, system: int, result: dict) -> None:
        """Runs the respective processes."""
        raise NotImplementedError()
