"""Common functions."""

from argparse import Namespace
from logging import DEBUG, INFO, WARNING
from subprocess import DEVNULL, PIPE, run, CompletedProcess
from typing import Iterable, Union

from homeinfotools.rpc.common import HOSTNAME, SSH, SSH_OPTIONS, SUDO


__all__ = [
    'completed_process_to_json',
    'execute',
    'ssh',
    'sudo',
    'get_log_level'
]


def completed_process_to_json(completed_process: CompletedProcess) -> dict:
    """Converts a completed process into a JSON-ish dict."""

    return {
        'args': completed_process.args,
        'returncode': completed_process.returncode,
        'stdout': completed_process.stdout,
        'stderr': completed_process.stderr,
    }


def execute(command: Union[str, Iterable[str]]) -> CompletedProcess:
    """Executes the given command."""

    return run(command, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, text=True,
               check=False)


def ssh(system: int, *command: str, no_stdin: bool = False) -> list[str]:
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


def sudo(*command: str) -> tuple[str]:
    """Runs the command as sudo."""

    return (SUDO, ' '.join(command))


def get_log_level(args: Namespace) -> int:
    """Returns the set logging level."""

    return DEBUG if args.debug else INFO if args.verbose else WARNING
