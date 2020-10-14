"""Reboots a system."""

from argparse import Namespace
from multiprocessing.managers import NamespaceProxy

from hidsl.logging import LOGGER
from hidsl.rpc.common import SYSTEMCTL
from hidsl.rpc.exceptions import OfflineError
from hidsl.rpc.functions import execute, ssh, sudo


__all__ = ['reboot']


def reboot(system: int, args: Namespace, job: NamespaceProxy) -> bool:
    """Reboots a system."""

    command = ssh(system, sudo(SYSTEMCTL, 'reboot'), no_stdin=args.no_stdin)
    completed_process = execute(command)
    job['reboot'] = completed_process.returncode

    if completed_process.returncode == 0:
        LOGGER.info('System %i is rebooting.')
        return True

    if completed_process.returncode == 1:
        LOGGER.warning('System %i may be rebooting.')
        return True

    if completed_process.returncode == 255:
        raise OfflineError(completed_process)

    return False
