"""Common functions."""

from argparse import Namespace
from logging import DEBUG, INFO, WARNING
from subprocess import DEVNULL, PIPE, run, CompletedProcess
from typing import Iterable, List, Tuple, Union

from hidsl.rpc.common import HOSTNAME, SSH, SSH_OPTIONS, SUDO


__all__ = ['execute', 'ssh', 'sudo', 'get_log_level']


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


def get_log_level(args: Namespace) -> int:
    """Returns the set logging level."""

    return DEBUG if args.debug else INFO if args.verbose else WARNING
