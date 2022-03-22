"""Processing of systems."""

from argparse import Namespace

from homeinfotools.multiprocessing import BaseWorker
from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker(BaseWorker):
    """Stored args and manager to process systems."""

    @staticmethod
    def run(system: int, args: Namespace) -> dict:
        """Runs the worker."""
        result = {}

        if args.sysupgrade:
            result['sysupgrade'] = sysupgrade(system, args)

        if args.execute:
            result['execute'] = runcmd(system, args)

        if args.reboot:
            result['reboot'] = reboot(system, args)

        return result
