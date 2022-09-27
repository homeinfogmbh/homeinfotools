"""Processing of systems."""

from homeinfotools.filetransfer.filetransfer import filetransfer
from homeinfotools.worker import BaseWorker


__all__ = ['Worker']


class Worker(BaseWorker):
    """Stored args and manager to process systems."""

    def run(self, system: int) -> dict:
        """Runs the worker."""
        return {'rsync': filetransfer(system, self.args)}
