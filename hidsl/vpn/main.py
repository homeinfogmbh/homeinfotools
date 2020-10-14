"""OpenVPN configuration package client."""

from logging import DEBUG, INFO, basicConfig
from sys import stdout

from hidsl.his import update_credentials, ErrorHandler
from hidsl.logging import LOG_FORMAT
from hidsl.vpn.argparse import get_args
from hidsl.vpn.functions import get_vpn_data


__all__ = ['main']


def main():
    """Main script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)
    user, passwd = update_credentials(args.user)

    with ErrorHandler('Error during VPN data retrieval.'):
        tar_file = get_vpn_data(user, passwd, args.system, args.windows)

    if args.file is None:
        stdout.buffer.write(tar_file)
    else:
        with args.file.open('wb') as file:
            file.write(tar_file)
