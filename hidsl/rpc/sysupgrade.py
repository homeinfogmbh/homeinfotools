"""System upgrade."""

from argparse import Namespace
from multiprocessing.managers import DictProxy
from subprocess import CompletedProcess

from hidsl.logging import LOGGER
from hidsl.rpc.common import PACMAN
from hidsl.rpc.exceptions import SSHConnectionError
from hidsl.rpc.exceptions import PacmanError
from hidsl.rpc.exceptions import SystemIOError
from hidsl.rpc.exceptions import UnknownError
from hidsl.rpc.functions import execute, ssh, sudo


__all__ = ['sysupgrade']


BY_RETURNCODE = {
    255: SSHConnectionError,
    126: SystemIOError,
    1: PacmanError
}


def get_exception(completed_process: CompletedProcess) -> Exception:
    """Raises an exception by the given
    the success status and return code.
    """

    try:
        exception = BY_RETURNCODE[completed_process.returncode]
    except KeyError:
        return UnknownError(completed_process)

    return exception(completed_process)


def upgrade_keyring(system: int, args: Namespace) -> CompletedProcess:
    """Upgrades the archlinux-keyring on that system."""

    command = [
        PACMAN, '-Sy', 'archlinux-keyring', '--needed', '--noconfirm',
        '--disable-download-timeout'
    ]
    command = sudo(*command)
    command = ssh(system, *command, no_stdin=args.no_stdin)
    LOGGER.debug('Executing command: %s', command)
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

    LOGGER.debug('Executing command: %s', command)
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

    LOGGER.debug('Executing command: %s', command)
    return execute(command)


def upgrade(system: int, args: Namespace, job: DictProxy):
    """Upgrade process function."""

    LOGGER.info('Upgrading system: %i', system)

    if args.keyring:
        completed_process = upgrade_keyring(system, args=args)
        job['keyring'] = completed_process.returncode

        if completed_process.returncode != 0:
            LOGGER.warning('Could not update keyring: %i', system)
            raise get_exception(completed_process)

    completed_process = upgrade_system(system, args=args)
    job['sysupgrade'] = completed_process.returncode

    if completed_process.returncode != 0:
        LOGGER.warning('Could not upgrade system: %i', system)
        raise get_exception(completed_process)

    if args.cleanup:
        completed_process = cleanup_system(system, args=args)
        job['pkgcleanup'] = completed_process.returncode

        if completed_process.returncode not in {0, 1}:
            LOGGER.warning('Could not clean up system: %i', system)
            raise get_exception(completed_process)


def sysupgrade(system: int, args: Namespace, job: DictProxy) -> bool:
    """Upgrated the respective system."""

    try:
        upgrade(system, args, job)
    except SystemIOError as error:
        LOGGER.error('I/O error: %i', system)
        LOGGER.debug('%s', error)
    except PacmanError as error:
        LOGGER.error('Pacman error: %i', system)
        LOGGER.debug('%s', error)
    except UnknownError as error:
        LOGGER.error('Unknown error: %i', system)
        LOGGER.debug('%s', error)
    else:
        return True

    return False
