"""Common functions."""

from argparse import Namespace
from datetime import datetime
from multiprocessing.managers import DictProxy
from os import linesep
from subprocess import DEVNULL, PIPE, run, CompletedProcess
from sys import argv, stderr
from typing import Iterable, List, Tuple, Union

from hidsl.logging import LOGGER
from hidsl.update.common import HOSTNAME, PACMAN, SSH, SSH_OPTIONS, SUDO
from hidsl.update.exceptions import OfflineError
from hidsl.update.exceptions import PacmanError
from hidsl.update.exceptions import UnknownError
from hidsl.update.exceptions import get_exception
from hidsl.update.proxy import UpdateJobProxy


__all__ = ['get_header', 'upgrade', 'print_finished', 'print_pending']


def execute(command: Union[Iterable[str], str]) -> CompletedProcess:
    """Executes the given command."""

    return run(command, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, text=True,
               check=False)


def ssh(system: int, *command: str, no_stdin: bool = False) -> List[str]:
    """Modifies the specified command to
    run via SSH on the specified system.
    """

    cmd = [SSH]

    if no_stdin:
        cmd.append('-n')

    for option in SSH_OPTIONS:
        cmd.append('-o')
        cmd.append(option)

    hostname = HOSTNAME.format(system)
    cmd.append(hostname)
    cmd.append(' '.join(command))
    return cmd


def sudo(*command: str) -> Tuple[str]:
    """Runs the command as sudo."""

    return (SUDO, ' '.join(command))


def get_header(comment: str = '#') -> Iterable[str]:
    """Yields header lines for the potential log file."""

    args = ' '.join(argv)
    now = datetime.now().isoformat()
    multiplier = 3 + 8 + max(len(args), len(now))
    yield comment * multiplier
    yield f'{comment}  Log of: {args}'
    yield f'{comment}  On:     {now}'
    yield comment * multiplier


def _upgrade_keyring(system: int, args: Namespace) -> CompletedProcess:
    """Upgrades the archlinux-keyring on that system."""

    command = [PACMAN, '-Sy', 'archlinux-keyring', '--needed', '--noconfirm']

    if not args.timeout:
        command.append('--disable-download-timeout')

    command = sudo(*command)
    command = ssh(system, *command, no_stdin=args.no_stdin)
    LOGGER.debug('Executing command: %s', command)
    return execute(command)


def _upgrade_system(system: int, args: Namespace) -> CompletedProcess:
    """Upgrades the system."""

    command = [PACMAN, '-Syu', '--needed']

    for package in args.package:
        command.append(package)

    for glob in args.overwrite:
        command.append('--overwrite')
        command.append(glob)

    if not args.timeout:
        command.append('--disable-download-timeout')

    if args.yes:
        command = 'yes | ' + ' '.join(sudo(*command))
        command = ssh(system, command, no_stdin=args.no_stdin)
    else:
        command.append('--noconfirm')
        command = sudo(*command)
        command = ssh(system, *command, no_stdin=args.no_stdin)

    LOGGER.debug('Executing command: %s', command)
    return execute(command)


def _cleanup_system(system: int, args: Namespace) -> CompletedProcess:
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


def _upgrade(system: int, args: Namespace, job: DictProxy):
    """Upgrade process function."""

    LOGGER.info('Upgrading system: %i', system)

    if args.keyring:
        completed_process = _upgrade_keyring(system, args=args)
        job.keyring = success = completed_process.returncode == 0

        if not success:
            LOGGER.error('Could not update keyring.')
            raise get_exception(completed_process)

    completed_process = _upgrade_system(system, args=args)
    job.sysupgrade = success = completed_process == 0

    if not success:
        LOGGER.error('Could not upgrade system.')
        raise get_exception(completed_process)

    if args.cleanup:
        completed_process = _cleanup_system(system, args=args)
        job.cleanup = success = completed_process in {0, 1}

        if not success:
            LOGGER.error('Could not clean up system.')
            raise get_exception(completed_process)


def upgrade(system: int, args: Namespace, jobs: DictProxy):
    """Upgrated the respective system."""

    with UpdateJobProxy(jobs[system]) as job:
        try:
            _upgrade(system, args, job)
        except OfflineError:
            LOGGER.error('System is offline.')
        except IOError:
            LOGGER.error('I/O error.')
        except PacmanError:
            LOGGER.error('Pacman error.')
        except UnknownError as error:
            LOGGER.error('Unknown error.')
            LOGGER.debug('%s', error)

    if args.logfile is not None:
        with args.logfile.open('a') as logfile:
            logfile.write(f'{system},' + job.to_csv() + linesep)


def print_finished(jobs, systems):
    """Prints pending jobs."""

    for system in systems:
        if not (proxy := UpdateJobProxy(jobs[system])).pending:
            print(system, 'ok' if proxy.success else 'failed', file=stderr)


def print_pending(jobs, systems):
    """Prints pending jobs."""

    pending = [sys for sys in systems if UpdateJobProxy(jobs[sys]).pending]
    text = ', '.join(str(system) for system in pending)
    print(text, file=stderr)
