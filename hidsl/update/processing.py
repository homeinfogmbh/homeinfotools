"""Processing of systems."""

from argparse import Namespace
from datetime import datetime
from multiprocessing import Manager
from multiprocessing.managers import DictProxy
from typing import NamedTuple, Tuple

from hidsl.logging import LOGGER
from hidsl.update.exceptions import OfflineError
from hidsl.update.reboot import reboot
from hidsl.update.runcmd import runcmd
from hidsl.update.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker(NamedTuple):
    """Stored args and manager to process systems."""

    args: Namespace
    manager: Manager

    def __call__(self, system: int) -> Tuple[int, DictProxy]:
        """Runs the worker on the given system."""
        job = self.manager.dict()
        job['start'] = datetime.now()
        success = True

        try:
            if self.args.sysupgrade and (self.args.force or success):
                success = sysupgrade(system, self.args, job)

            if self.args.execute and (self.args.force or success):
                success = runcmd(system, self.args, job)

            if self.args.reboot and (self.args.force or success):
                success = reboot(system, self.args, job)
        except OfflineError as error:
            LOGGER.error('System is offline: %i', system)
            LOGGER.info('%s', error)

        job['success'] = success
        job['end'] = datetime.now()
        return (system, job)
