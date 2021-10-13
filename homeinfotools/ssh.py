"""SSH command."""

from typing import Optional

from homeinfotools.os import SSH


__all__ = ['ssh']


HOSTNAME = '{}.terminals.homeinfo.intra'
SSH_OPTIONS = [
    'LogLevel=error',
    'UserKnownHostsFile=/dev/null',
    'StrictHostKeyChecking=no',
    'ConnectTimeout=5'
]


def ssh(system: Optional[int], *command: str,
        no_stdin: bool = False) -> list[str]:
    """Modifies the specified command to
    run via SSH on the specified system.
    """

    cmd = [SSH]

    if no_stdin:
        cmd.append('-n')

    for option in SSH_OPTIONS:
        cmd.append('-o')
        cmd.append(option)

    if system is not None:
        cmd.append(HOSTNAME.format(system))

    if command:
        cmd.append(' '.join(command))

    return cmd
