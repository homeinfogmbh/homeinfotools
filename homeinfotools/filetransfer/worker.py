"""Processing of systems."""

from argparse import Namespace

from homeinfotools.filetransfer.filetransfer import filetransfer
from homeinfotools.multiprocessing import BaseWorker


__all__ = ['Worker']


class Worker(BaseWorker):
    """Stored args and manager to process systems."""

    @staticmethod
    def run(system: int, args: Namespace) -> dict:
        """Runs the worker."""
        return {'rsync': filetransfer(system, args)}
