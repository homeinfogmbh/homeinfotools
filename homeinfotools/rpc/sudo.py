"""Sudo command handling."""


__all__ = ['sudo']


SUDO = '/usr/bin/sudo'


def sudo(*command: str) -> tuple[str, str]:
    """Runs the command as sudo."""

    return SUDO, ' '.join(command)
