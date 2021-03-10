"""Processing of systems."""

from argparse import Namespace
from datetime import datetime

from homeinfotools.logging import syslogger
from homeinfotools.rpc.exceptions import SSHConnectionError
from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker:   # pylint: disable=R0903
    """Stored args and manager to process systems."""

    __slots__ = ('args',)

    def __init__(self, args: Namespace):
        """Sets the command line arguments."""
        self.args = args

    def __call__(self, system: int) -> tuple[int, dict]:
        """Runs the worker on the given system."""
        start = datetime.now()
        result = {'start': start.isoformat()}
        success = True

        try:
            if self.args.sysupgrade:
                result['sysupgrade'] = sysupgrade(system, self.args)

            if self.args.execute:
                result['execute'] = runcmd(system, self.args)

            if self.args.reboot:
                result['reboot'] = reboot(system, self.args)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')

        result['success'] = success
        end = datetime.now()
        result['end'] = end.isoformat()
        result['duration'] = str(end - start)
        return (system, result)
