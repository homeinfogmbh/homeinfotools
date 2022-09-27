"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('args', 'results')

    def __init__(self, args: Namespace, results: dict):
        """Sets the command line arguments."""
        self.args = args
        self.results = results

    def __call__(self, system: int):
        """Processes a single system."""
        setproctitle(f'hidsltools-worker@{system}')
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
        self.results[system] = result

    def run(self, system: int) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()
