"""Processing of systems."""

from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade
from homeinfotools.worker import BaseWorker


__all__ = ['Worker']


class Worker(BaseWorker):
    """Stored args and manager to process systems."""

    def run(self) -> dict:
        """Runs the worker."""
        result = {}

        if self.args.sysupgrade:
            result['sysupgrade'] = sysupgrade(self.system, self.args)

        if self.args.execute:
            result['execute'] = runcmd(self.system, self.args)

        if self.args.reboot:
            result['reboot'] = reboot(self.system, self.args)

        return result
