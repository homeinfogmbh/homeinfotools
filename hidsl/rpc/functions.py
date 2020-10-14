"""Common functions."""

from argparse import Namespace
from datetime import datetime
from logging import DEBUG, ERROR, INFO, WARNING
from subprocess import DEVNULL, PIPE, run, CompletedProcess
from sys import argv
from typing import Iterable, List, Tuple, Union

from hidsl.rpc.common import HOSTNAME, SSH, SSH_OPTIONS, SUDO


__all__ = ['get_header', 'get_log_level']


RED = '\\e[31m{}\\e[0m'


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


def get_configuration(args: Namespace) -> Iterable[str]:
    """Yields configurations from the given arguments."""

    args = args._get_kwargs()   # pylint: disable=W0212
    maxlen = max(len(key) for key, _ in args)

    for key, value in args:
        padding = maxlen - len(key)
        yield f'{key}' + ' ' * padding + f' = {value}'


def get_header(args: Namespace, *, comment: str = '#') -> Iterable[str]:
    """Yields header lines for the potential log file."""

    yield comment * 79
    yield f'{comment}  Log of {argv[0]} run on {datetime.now()}.'
    yield f'{comment}  Configuration:'

    for line in get_configuration(args):
        yield f'{comment}    {line}'

    yield comment * 79


def get_log_level(args: Namespace) -> int:
    """Returns the set logging level."""

    if args.debuglevel > 0:
        return INFO

    if args.debuglevel > 1:
        return DEBUG

    return WARNING if args.verbose else ERROR
