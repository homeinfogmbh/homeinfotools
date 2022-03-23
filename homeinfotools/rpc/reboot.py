"""Reboots a system."""

from argparse import Namespace

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.functions import completed_process_to_json, execute
from homeinfotools.logging import syslogger
from homeinfotools.rpc.common import SYSTEMCTL
from homeinfotools.rpc.sudo import sudo
from homeinfotools.ssh import ssh


__all__ = ['reboot']


def reboot(system: int, args: Namespace) -> dict:
    """Reboots a system."""

    command = ssh(system, *sudo(SYSTEMCTL, 'reboot'), no_stdin=args.no_stdin)
    syslogger(system).debug('Rebooting system %i.', system)
    completed_process = execute(command)

    if completed_process.returncode == 0:
        syslogger(system).info('System %i is rebooting.', system)
    elif completed_process.returncode == 1:
        syslogger(system).warning('System %i may be rebooting.', system)
    elif completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    return completed_process_to_json(completed_process)
