"""HIS SSO API."""

from getpass import getpass
from sys import exit    # pylint: disable=W0622
from typing import Optional

from homeinfotools.logging import LOGGER


__all__ = ['update_credentials']


def update_credentials(account: Optional[str],
                       passwd: Optional[str] = None) -> tuple[str, str]:
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
