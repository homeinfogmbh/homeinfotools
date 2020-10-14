"""Execute commands on a remote system."""

from argparse import Namespace
from multiprocessing.managers import DictProxy

from hidsl.logging import LOGGER
from hidsl.rpc.exceptions import OfflineError
from hidsl.rpc.functions import execute, ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace, job: DictProxy) -> bool:
    """Runs commands on a remote system."""

    result = True

    for index, commandline in enumerate(args.execute, start=1):
        command = ssh(system, commandline, no_stdin=args.no_stdin)
        LOGGER.debug('Running "%s" on system %i.', commandline, system)
        completed_process = execute(command)
        job[commandline] = success = completed_process.returncode == 0

        if completed_process.returncode == 255:
            raise OfflineError(completed_process)

        LOGGER.debug('Command returned %i.', completed_process.returncode)

        if stdout := completed_process.stdout:
            LOGGER.info('System %i: %s -> %s', system, commandline, stdout)

        if stderr := completed_process.stderr:
            LOGGER.warning('System %i: %s -> %s', system, commandline, stderr)

        if not success:
            result = False
            LOGGER.error('Command #%i failed on system %i.', index, system)
            LOGGER.debug('STDOUT: %s', completed_process.stdout)
            LOGGER.debug('STDERR: %s', completed_process.stderr)

    return result
