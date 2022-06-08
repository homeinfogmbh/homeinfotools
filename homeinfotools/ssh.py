"""SSH command."""

from functools import cache
from pathlib import Path
from subprocess import DEVNULL, CalledProcessError, check_call

from homeinfotools.os import SSH, RSYNC


__all__ = ['ssh', 'rsync']


HOSTNAME = '{}.terminals.homeinfo.intra'
SSH_OPTIONS = [
    'LogLevel=error',
    'UserKnownHostsFile=/dev/null',
    'StrictHostKeyChecking=no',
    'ConnectTimeout=5'
]
TRUE = '/usr/bin/true'
USERS = {'homeinfo', 'root'}
HostPath = Path | tuple[int, Path]


def ssh(
        system: int | None,
        *command: str,
        user: str | None = None,
        no_stdin: bool = False
) -> list[str]:
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
        if user is None:
            user = get_ssh_user(system)

        hostname = HOSTNAME.format(system)

        if user is not None:
            hostname = f'{user}@{hostname}'

        cmd.append(hostname)

    if command:
        cmd.append(' '.join(command))

    return cmd


def rsync(
        src: HostPath,
        dst: HostPath,
        *,
        all: bool = True,
        update: bool = True,
        verbose: bool = True
) -> list[str]:
    """Returns the respective rsync command."""

    cmd = [RSYNC, '-e', ' '.join(ssh(None))]

    if all:
        cmd.append('-a')

    if update:
        cmd.append('-u')

    if verbose:
        cmd.append('-v')

    return cmd + [get_remote_path(src), get_remote_path(dst)]


def get_remote_path(path: HostPath) -> str:
    """Returns a host path."""

    try:
        system, path = path
    except TypeError:
        return path

    return HOSTNAME.format(f'{get_ssh_user(system)}@{system}') + f':{path}'


@cache
def get_ssh_user(system: int) -> str | None:
    """Returns the SSH user."""

    for user in USERS:
        try:
            check_call(
                ssh(system, TRUE, user=user),
                stdout=DEVNULL,
                stderr=DEVNULL
            )
        except CalledProcessError:
            continue

        return user

    return None
