"""Execute commands on a remote system."""

from argparse import Namespace
from multiprocessing.managers import DictProxy

from hidsl.logging import LOGGER
from hidsl.rpc.exceptions import SSHConnectionError
from hidsl.rpc.functions import execute, ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace, job: DictProxy) -> bool:
    """Runs commands on a remote system."""

    command = ssh(system, args.execute, no_stdin=args.no_stdin)
    LOGGER.debug('Running "%s" on system %i.', args.execute, system)
    completed_process = execute(command)
    job['command'] = completed_process.returncode

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    LOGGER.debug('Command returned %i.', completed_process.returncode)

    if stdout := completed_process.stdout:
        LOGGER.info('System %i: %s', system, stdout.strip())

    if stderr := completed_process.stderr:
        LOGGER.warning('System %i: %s', system, stderr.strip())

    if not (success := completed_process.returncode == 0):
        LOGGER.error('Command failed on system %i.', system)

    return success
