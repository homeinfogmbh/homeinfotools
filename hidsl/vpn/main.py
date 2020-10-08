"""OpenVPN configuration package client."""

from logging import DEBUG, INFO, basicConfig
from sys import exit, stdout    # pylint: disable=W0622

from hidsl.logging import LOG_FORMAT, LOGGER
from hidsl.vpn.argparse import get_args
from hidsl.vpn.exceptions import DownloadError, LoginError
from hidsl.vpn.functions import read_credentials, get_vpn_data


__all__ = ['main']


def main():
    """Main script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)
    user, passwd = read_credentials(args.user)

    try:
        tar_file = get_vpn_data(user, passwd, args.system, args.windows)
    except LoginError as error:
        LOGGER.error('Error during login.')
        LOGGER.debug(error)
        exit(2)
    except DownloadError as error:
        LOGGER.error('Error during VPN data retrieval.')
        LOGGER.debug(error)
        exit(3)

    if args.file is None:
        stdout.buffer.write(tar_file)
    else:
        with args.file.open('wb') as file:
            file.write(tar_file)
