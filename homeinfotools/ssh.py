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
HostPath = Path | tuple[int, Path]


def ssh(
        system: int | None,
        *command: str,
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
        cmd.append(HOSTNAME.format(system))

    if command:
        cmd.append(' '.join(command))

    return cmd


def get_remote_path(path: HostPath) -> str:
    """Returns a host path."""

    try:
        system, path = path
    except TypeError:
        return path

    return HOSTNAME.format(system) + f':{path}'


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
