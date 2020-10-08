"""OpenVPN configuration package client."""

from getpass import getpass
from logging import DEBUG, INFO, basicConfig
from sys import exit    # pylint: disable=W0622

from hidsl.logging import LOG_FORMAT, LOGGER
from hidsl.vpn.argparse import get_args
from hidsl.vpn.functions import retrieve_data


__all__ = ['main']


def main():
    """Main script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)

    if args.user:
        user = args.user
    else:
        try:
            user = input('User name: ')
        except (EOFError, KeyboardInterrupt):
            print()
            LOGGER.error('Aborted by user.')
            exit(1)

    try:
        passwd = getpass('Password: ')
    except (EOFError, KeyboardInterrupt):
        print()
        LOGGER.error('Aborted by user.')
        exit(1)

    login_data = {'account': user, 'passwd': passwd}
    vpn_data = {'system': args.system, 'windows': args.windows}
    retrieve_data(login_data, vpn_data, args.file)
