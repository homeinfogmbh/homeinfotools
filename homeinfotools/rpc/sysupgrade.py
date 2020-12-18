"""System upgrade."""

from argparse import Namespace
from subprocess import CompletedProcess

from homeinfotools.logging import syslogger
from homeinfotools.rpc.common import PACMAN
from homeinfotools.rpc.exceptions import SSHConnectionError
from homeinfotools.rpc.exceptions import PacmanError
from homeinfotools.rpc.exceptions import SystemIOError
from homeinfotools.rpc.exceptions import UnknownError
from homeinfotools.rpc.functions import completed_process_to_json
from homeinfotools.rpc.functions import execute
from homeinfotools.rpc.functions import ssh
from homeinfotools.rpc.functions import sudo


__all__ = ['sysupgrade']


def lograise(system: int, message: str, completed_process: CompletedProcess):
    """Issues a warning message and raises an exception."""

    if completed_process.returncode == 255:
        raise SSHConnectionError(completed_process)

    # Do not warn on SSH connection errors.
    syslogger(system).warning(message)

    if completed_process.returncode == 126:
        raise SystemIOError(completed_process)

    if completed_process.returncode == 1:
        raise PacmanError(completed_process)

    raise UnknownError(completed_process)


def upgrade_keyring(system: int, args: Namespace) -> CompletedProcess:
    """Upgrades the archlinux-keyring on that system."""

    command = [
        PACMAN, '-Sy', 'archlinux-keyring', '--needed', '--noconfirm',
        '--disable-download-timeout'
    ]
    command = sudo(*command)
    command = ssh(system, *command, no_stdin=args.no_stdin)
    syslogger(system).debug('Executing command: %s', command)
    return execute(command)


def upgrade_system(system: int, args: Namespace) -> CompletedProcess:
    """Upgrades the system."""

    command = [PACMAN, '-Syu', '--needed', '--disable-download-timeout']

    for package in args.install:
        command.append(package)

    for glob in args.overwrite:
        command.append('--overwrite')
        command.append(glob)

    if args.yes:
        command = 'yes | ' + ' '.join(sudo(*command))
        command = ssh(system, command, no_stdin=args.no_stdin)
    else:
        command.append('--noconfirm')
        command = sudo(*command)
        command = ssh(system, *command, no_stdin=args.no_stdin)

    syslogger(system).debug('Executing command: %s', command)
    return execute(command)


def cleanup_system(system: int, args: Namespace) -> CompletedProcess:
    """Cleans up the system."""

    command = [PACMAN, '-Rncs', '$(pacman -Qmq)', '$(pacman -Qdtq)']

    if args.yes:
        command = 'yes | ' + ' '.join(sudo(*command))
        command = ssh(system, command, no_stdin=args.no_stdin)
    else:
        command.append('--noconfirm')
        command = sudo(*command)
        command = ssh(system, *command, no_stdin=args.no_stdin)

    syslogger(system).debug('Executing command: %s', command)
    return execute(command)


def upgrade(system: int, args: Namespace):
    """Upgrade process function."""

    syslogger(system).info('Upgrading system.')
    result = {}

    if args.keyring:
        completed_process = upgrade_keyring(system, args=args)
        result['keyring'] = completed_process_to_json(completed_process)

        if completed_process.returncode != 0:
            lograise(system, 'Could not update keyring.', completed_process)

    completed_process = upgrade_system(system, args=args)
    result['sysupgrade'] = completed_process_to_json(completed_process)

    if completed_process.returncode != 0:
        lograise(system, 'Could not upgrade system.', completed_process)

    if args.cleanup:
        completed_process = cleanup_system(system, args=args)
        result['pkgcleanup'] = completed_process_to_json(completed_process)

        if completed_process.returncode not in {0, 1}:
            lograise(system, 'Could not clean up system.', completed_process)

    return result


def sysupgrade(system: int, args: Namespace) -> bool:
    """Upgrated the respective system."""

    try:
        return upgrade(system, args)
    except SystemIOError as error:
        syslogger(system).error('I/O error.')
        syslogger(system).debug('%s', error)
        return completed_process_to_json(error.completed_process)
    except PacmanError as error:
        syslogger(system).error('Pacman error.')
        syslogger(system).debug('%s', error)
        return completed_process_to_json(error.completed_process)
    except UnknownError as error:
        syslogger(system).error('Unknown error.')
        syslogger(system).debug('%s', error)
        return completed_process_to_json(error.completed_process)
