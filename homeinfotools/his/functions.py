"""HIS SSO API."""

from getpass import getpass
from sys import exit

from homeinfotools.logging import LOGGER


__all__ = ['update_credentials']


def update_credentials(
        account: str | None,
        passwd: str | None = None
) -> tuple[str, str]:
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

    return account, passwd
