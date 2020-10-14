"""Execute commands on a remote system."""

from argparse import Namespace
from multiprocessing.managers import DictProxy

from hidsl.logging import LOGGER
from hidsl.update.exceptions import OfflineError
from hidsl.update.functions import execute, ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace, job: DictProxy) -> bool:
    """Runs commands on a remote system."""

    result = True

    for index, command in enumerate(args.execute, start=1):
        command = ssh(system, command, no_stdin=args.no_stdin)
        completed_process = execute(command)
        job[command] = success = completed_process.returncode == 0

        if completed_process.returncode == 255:
            raise OfflineError(completed_process)

        if not success:
            result = False
            LOGGER.debug('Running "%s" on system %i.', command, system)
            LOGGER.error('Command #%i failed on system %i.', index, system)
            LOGGER.info('Command returned %i.', completed_process.returncode)
            LOGGER.debug('STDOUT: %s', completed_process.stdout)
            LOGGER.debug('STDERR: %s', completed_process.stderr)

    return result
