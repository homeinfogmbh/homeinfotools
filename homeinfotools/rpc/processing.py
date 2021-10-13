"""Processing of systems."""

from homeinfotools.worker import BaseWorker
from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker(BaseWorker):   # pylint: disable=R0903
    """Stored args and manager to process systems."""

    def run(self, system: int, result: dict) -> None:
        """Runs the worker."""
        if self.args.sysupgrade:
            result['sysupgrade'] = sysupgrade(system, self.args)

        if self.args.execute:
            result['execute'] = runcmd(system, self.args)

        if self.args.reboot:
            result['reboot'] = reboot(system, self.args)
