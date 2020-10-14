"""Common constants."""

from getpass import getpass
from sys import exit    # pylint: disable=W0622
from typing import Tuple

from requests import session

from hidsl.logging import LOGGER


__all__ = [
    'DownloadError',
    'LoginError',
    'update_credentials',
    'HISSession',
    'ErrorHandler'
]


HIS_LOGIN_URL = 'https://his.homeinfo.de/session'


class WebAPIError(Exception):
    """A web API error."""

    def __init__(self, response):
        """Sets the response."""
        super().__init__(response)
        self.response = response

    def __str__(self):
        """Returns the content as string."""
        return self.response.text


class DownloadError(WebAPIError):
    """Indicates an error during data download."""


class LoginError(WebAPIError):
    """Indicates an error during login."""


def update_credentials(account: str, passwd: str = None) -> Tuple[str, str]:
    """Reads the credentials for a HIS account."""

    if not account:
        try:
            account = input('User name: ')
        except (EOFError, KeyboardInterrupt):
            print()
            LOGGER.error('Aborted by user.')
            exit(1)

    if not passwd:
        try:
            passwd = getpass('Password: ')
        except (EOFError, KeyboardInterrupt):
            print()
            LOGGER.error('Aborted by user.')
            exit(1)

    return (account, passwd)


class HISSession:
    """A HIS session."""

    def __init__(self, account: str, passwd: str):
        """Sets account name and password."""
        self.account = account
        self.passwd = passwd
        self.session = session()
        self.session_guard = None

    def __enter__(self):
        self.session_guard = self.session.__enter__()
        self.login()
        return self

    def __exit__(self, *args):
        return self.session.__exit__(*args)

    def __getattr__(self, attr):
        """Delegates to the session object."""
        return getattr(self.session_guard, attr)

    @property
    def credentials(self):
        """Returns the login credentials as JSON."""
        return {'account': self.account, 'passwd': self.passwd}

    def login(self):
        """Performs a login."""
        response = self.post(HIS_LOGIN_URL, json=self.credentials)

        if response.status_code != 200:
            raise LoginError(response)

        return True

    def get_json(self, url):
        """Returns a JSON-ish dict."""
        response = self.get(url)

        if response.status_code != 200:
            raise DownloadError(response)

        return response.json


class ErrorHandler:
    """Handles login and download errors."""

    def __init__(self, download_error_text: str):
        """Sets the download error text."""
        self.download_error_text = download_error_text

    def __enter__(self):
        return self

    def __exit__(self, typ, value, _):
        """Handles login and download errors."""
        if typ is LoginError:
            LOGGER.error('Error during login.')
            LOGGER.debug(value)
            exit(2)

        if typ is DownloadError:
            LOGGER.error(self.download_error_text)
            LOGGER.debug(value)
            exit(3)
