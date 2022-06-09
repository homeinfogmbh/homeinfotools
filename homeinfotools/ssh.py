"""SSH command."""

from pathlib import Path

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
        user: str | None = None,
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

    return [
        *cmd,
        get_remote_path(src, user=user),
        get_remote_path(dst, user=user)
    ]


def get_remote_path(path: HostPath, *, user: str | None = None) -> str:
    """Returns a host path."""

    try:
        system, path = path
    except TypeError:
        return path

    return ':'.join([
        HOSTNAME.format(system if user is None else f'{user}@{system}'),
        str(path)
    ])
