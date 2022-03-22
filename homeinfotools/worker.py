"""Multiprocessing worker."""

from argparse import Namespace
from collections import defaultdict
from datetime import datetime
from multiprocessing import Queue
from queue import Empty

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('args', 'systems', 'results')

    def __init__(self, args: Namespace, systems: Queue[int]):
        """Sets the command line arguments."""
        self.args = args
        self.systems = systems
        self.results = defaultdict(dict)

    def __call__(self) -> None:
        """Runs the worker on the given system."""
        while True:
            try:
                system = self.systems.get_nowait()
            except Empty:
                return

            self._process_system(system, self.results[system])

    def _process_system(self, system: int, result: dict) -> None:
        """Processes a single system."""
        result['start'] = (start := datetime.now()).isoformat()

        try:
            result['result'] = self.run(system)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')
            result['success'] = False
        else:
            result['success'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)

    def run(self, system: int) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()
