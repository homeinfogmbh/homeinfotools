"""HIS SSO API."""

from sys import exit    # pylint: disable=W0622

from homeinfotools.his.exceptions import DownloadError, LoginError
from homeinfotools.logging import LOGGER


__all__ = ['ErrorHandler']


class ErrorHandler:
    """Handles login and download errors."""

    def __init__(self, error_text: str):
        """Sets the download error text."""
        self.error_text = error_text

    def __enter__(self):
        return self

    def __exit__(self, typ, value, _):
        """Handles login and download errors."""
        if typ is LoginError:
            LOGGER.error('Error during login.')
            LOGGER.debug(value)
            exit(2)

        if typ is DownloadError:
            LOGGER.error(self.error_text)
            LOGGER.debug(value)
            exit(3)
