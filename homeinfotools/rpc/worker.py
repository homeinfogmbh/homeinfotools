"""Processing of systems."""

from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade
from homeinfotools.worker import BaseWorker


__all__ = ['Worker']


class Worker(BaseWorker):
    """Stored args and manager to process systems."""

    def run(self, system: int) -> dict:
        """Runs the worker."""
        result = {}

        if self.args.sysupgrade:
            result['sysupgrade'] = sysupgrade(system, self.args)

        if self.args.execute:
            result['execute'] = runcmd(system, self.args)

        if self.args.reboot:
            result['reboot'] = reboot(system, self.args)

        return result
