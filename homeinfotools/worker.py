"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime
from logging import INFO, Logger, getLogger
from typing import Callable

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('system', 'args', 'results')

    def __init__(self, system: int, args: Namespace, results: dict):
        """Sets the command line arguments."""
        self.system = system
        self.args = args
        self.results = results

    def __call__(self):
        """Processes a single system."""
        setproctitle(self.name)
        result = {'start': (start := datetime.now()).isoformat()}

        try:
            result['result'] = self.run()
        except SSHConnectionError:
            syslogger(self.system).error('Could not establish SSH connection.')
            result['online'] = False
        else:
            result['online'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)
        self.results[self.system] = result

    @classmethod
    def spawner(cls, args: Namespace, results: dict) -> Callable[[int], None]:
        """Wrapper to spawn workers."""
        return lambda system: cls(system, args=args, results=results)()

    @property
    def logger(self) -> Logger:
        """Returns the worker's logger."""
        logger = getLogger(self.name)
        logger.setLevel(INFO)
        return logger

    @property
    def name(self) -> str:
        """Returns the worker's name."""
        return f'hidsltools-worker@{self.system}'

    def run(self) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()
