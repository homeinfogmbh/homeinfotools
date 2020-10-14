"""Execute commands on a remote system."""

from argparse import Namespace
from multiprocessing.managers import DictProxy

from hidsl.logging import LOGGER
from hidsl.rpc.exceptions import OfflineError
from hidsl.rpc.functions import execute, ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace, job: DictProxy) -> bool:
    """Runs commands on a remote system."""

    command = ssh(system, args.execute, no_stdin=args.no_stdin)
    LOGGER.debug('Running "%s" on system %i.', args.execute, system)
    completed_process = execute(command)
    job[args.execute] = success = completed_process.returncode == 0

    if completed_process.returncode == 255:
        raise OfflineError(completed_process)

    LOGGER.debug('Command returned %i.', completed_process.returncode)

    if stdout := completed_process.stdout:
        LOGGER.info('System %i: %s', system, stdout)

    if stderr := completed_process.stderr:
        LOGGER.warning('System %i: %s', system, stderr)

    if not success:
        LOGGER.error('Command failed on system %i.', system)

    return success
