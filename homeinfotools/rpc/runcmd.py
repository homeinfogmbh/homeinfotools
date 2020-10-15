"""Execute commands on a remote system."""

from argparse import Namespace

from homeinfotools.logging import LOGGER
from homeinfotools.rpc.exceptions import SSHConnectionError
from homeinfotools.rpc.functions import completed_process_to_json, execute, ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace) -> bool:
    """Runs commands on a remote system."""

    command = ssh(system, args.execute, no_stdin=args.no_stdin)
    LOGGER.debug('Running "%s" on system %i.', args.execute, system)
    completed_process = execute(command)

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    LOGGER.debug('Command returned %i.', completed_process.returncode)

    if stdout := completed_process.stdout:
        LOGGER.info('System %i: %s', system, stdout.strip())

    if stderr := completed_process.stderr:
        LOGGER.warning('System %i: %s', system, stderr.strip())

    if not completed_process.returncode == 0:
        LOGGER.error('Command failed on system %i.', system)

    return completed_process_to_json(completed_process)
