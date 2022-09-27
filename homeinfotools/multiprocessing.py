"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime
from logging import INFO, Logger, getLogger
from multiprocessing import Queue
from queue import Empty
from typing import Any, Iterator

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker', 'consume']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('results', 'args', 'system')

    def __init__(self, results: Queue, args: Namespace):
        """Sets the command line arguments."""
        self.results = results
        self.args = args
        self.system = None

    def __call__(self, system: int) -> None:
        """Runs the worker on the given system."""
        setproctitle(self.name)
        result = self.process_system(system)
        self.results.put_nowait((system, result))
        self.logger.info('Aborted')

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

    def process_system(self, system: int) -> dict:
        """Processes a single system."""
        result = {'start': (start := datetime.now()).isoformat()}

        try:
            result['result'] = self.run(system)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')
            result['online'] = False
        else:
            result['online'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)
        return result

    def run(self, system: int) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()


def consume(queue: Queue) -> Iterator[Any]:
    """Iterates over a queue until it is empty."""

    while True:
        try:
            yield queue.get_nowait()
        except Empty:
            break
