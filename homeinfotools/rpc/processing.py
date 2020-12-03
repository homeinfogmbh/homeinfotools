"""Processing of systems."""

from argparse import Namespace
from datetime import datetime
from multiprocessing.managers import DictProxy
from typing import NamedTuple, Tuple

from homeinfotools.logging import syslogger
from homeinfotools.rpc.exceptions import SSHConnectionError
from homeinfotools.rpc.reboot import reboot
from homeinfotools.rpc.runcmd import runcmd
from homeinfotools.rpc.sysupgrade import sysupgrade


__all__ = ['Worker']


class Worker(NamedTuple):
    """Stored args and manager to process systems."""

    args: Namespace

    def __call__(self, system: int) -> Tuple[int, DictProxy]:
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
