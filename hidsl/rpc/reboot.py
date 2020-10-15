"""Reboots a system."""

from argparse import Namespace
from multiprocessing.managers import NamespaceProxy

from hidsl.logging import LOGGER
from hidsl.rpc.common import SYSTEMCTL
from hidsl.rpc.exceptions import SSHConnectionError
from hidsl.rpc.functions import execute, ssh, sudo


__all__ = ['reboot']


def reboot(system: int, args: Namespace, job: NamespaceProxy) -> bool:
    """Reboots a system."""

    command = ssh(system, *sudo(SYSTEMCTL, 'reboot'), no_stdin=args.no_stdin)
    LOGGER.debug('Rebooting system %i.', system)
    completed_process = execute(command)
    job['reboot'] = completed_process.returncode

    if completed_process.returncode == 0:
        LOGGER.info('System %i is rebooting.', system)
        return True

    if completed_process.returncode == 1:
        LOGGER.warning('System %i may be rebooting.', system)
        return True

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    return False
