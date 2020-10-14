"""Common constants."""

from os import name


__all__ = ['HOSTNAME', 'PACMAN', 'SUDO', 'SSH', 'SSH_OPTIONS', 'SYSTEMCTL']


HOSTNAME = '{}.terminals.homeinfo.intra'
PACMAN = '/usr/bin/pacman'

if name == 'posix':
    SSH = '/usr/bin/ssh'
elif name == 'nt':
    SSH = '/usr/bin/ssh'
else:
    raise OSError('Unsupported operating system.')

SSH_OPTIONS = (
    'LogLevel=error', 'UserKnownHostsFile=/dev/null',
    'StrictHostKeyChecking=no', 'ConnectTimeout=5'
)
SUDO = '/usr/bin/sudo'
SYSTEMCTL = '/usr/bin/systemctl'
