"""Common constants."""

from homeinfotools.os import SSH


__all__ = [
    'HOSTNAME',
    'PACMAN',
    'SUDO',
    'SSH',
    'SSH_OPTIONS',
    'SYSTEMCTL'
]


HOSTNAME = '{}.terminals.homeinfo.intra'
PACMAN = '/usr/bin/pacman'
SSH_OPTIONS = [
    'LogLevel=error',
    'UserKnownHostsFile=/dev/null',
    'StrictHostKeyChecking=no',
    'ConnectTimeout=5'
]
SUDO = '/usr/bin/sudo'
SYSTEMCTL = '/usr/bin/systemctl'
