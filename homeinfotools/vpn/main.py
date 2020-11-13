"""OpenVPN configuration package client."""

from logging import DEBUG, INFO, basicConfig
from sys import stdout

from homeinfotools.his import update_credentials, ErrorHandler
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.vpn.argparse import get_args
from homeinfotools.vpn.functions import configure


__all__ = ['main']


def main():
    """Main script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)
    user, passwd = update_credentials(args.user)

    with ErrorHandler('Error during VPN data retrieval.'):
        tar_file = configure(user, passwd, args)

    if args.file is None:
        stdout.buffer.write(tar_file)
    else:
        with args.file.open('wb') as file:
            file.write(tar_file)
