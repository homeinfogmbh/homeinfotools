"""Processing of systems."""

from homeinfotools.filetransfer.filetransfer import filetransfer
from homeinfotools.worker import BaseWorker


__all__ = ['Worker']


class Worker(BaseWorker):   # pylint: disable=R0903
    """Stored args and manager to process systems."""

    def run(self, system: int, result: dict) -> None:
        """Runs the worker."""
        result['sysupgrade'] = filetransfer(system, self.args)
