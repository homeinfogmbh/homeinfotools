"""Processing of systems."""

from argparse import Namespace
from datetime import datetime
from multiprocessing.managers import DictProxy
from typing import NamedTuple, Tuple

from homeinfotools.logging import LOGGER
from homeinfotools.rpc.exceptions import SSHConnectionError
from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker(NamedTuple):
    """Stored args and manager to process systems."""

    args: Namespace
    jobs: DictProxy

    def __call__(self, system: int) -> Tuple[int, DictProxy]:
        """Runs the worker on the given system."""
        job = self.jobs[system]
        job['start'] = datetime.now()
        success = True

        try:
            if self.args.sysupgrade:
                success = sysupgrade(system, self.args, job)

            if self.args.execute and success:
                success = runcmd(system, self.args, job)

            if self.args.reboot and success:
                success = reboot(system, self.args, job)
        except SSHConnectionError:
            LOGGER.error('Could not establish SSH connection with %i.', system)

        job['success'] = success
        job['end'] = datetime.now()
