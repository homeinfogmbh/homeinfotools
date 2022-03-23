"""Execute commands on a remote system."""

from argparse import Namespace

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger
from homeinfotools.functions import completed_process_to_json, execute
from homeinfotools.ssh import ssh


__all__ = ['runcmd']


def runcmd(system: int, args: Namespace) -> dict:
    """Runs commands on a remote system."""

    command = ssh(system, args.execute, no_stdin=args.no_stdin)
    syslogger(system).debug('Running "%s" on system.', args.execute)
    completed_process = execute(command)

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    syslogger(system).debug('Returncode: %i', completed_process.returncode)

    if stdout := completed_process.stdout:
        syslogger(system).info(stdout.strip())

    if stderr := completed_process.stderr:
        syslogger(system).warning(stderr.strip())

    if not completed_process.returncode == 0:
        syslogger(system).error('Command failed.')

    return completed_process_to_json(completed_process)
