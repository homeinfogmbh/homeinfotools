"""Common exceptions."""

from homeinfotools.exceptions import RemoteProcessError


__all__ = ['SystemIOError', 'PacmanError', 'UnknownError']


class SystemIOError(RemoteProcessError):
    """Indicates an I/O error on the remote system."""


class PacmanError(RemoteProcessError):
    """Indicates an error with pacman."""


class UnknownError(RemoteProcessError):
    """Indicates an unknown error."""
