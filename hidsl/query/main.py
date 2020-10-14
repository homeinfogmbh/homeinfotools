"""Main script."""

from logging import DEBUG, INFO, WARNING, basicConfig

from hidsl.his import update_credentials, ErrorHandler
from hidsl.logging import LOG_FORMAT, LOGGER
from hidsl.query.argparse import get_args
from hidsl.query.functions import filter_systems, get_systems


__all__ = ['main']


def main():
    """Runs the script."""

    args = get_args()
    loglevel = DEBUG if args.debug else INFO if args.verbose else WARNING
    basicConfig(format=LOG_FORMAT, level=loglevel)
    user, passwd = update_credentials(args.user)
    LOGGER.info('Retrieving systems.')

    with ErrorHandler('Error during JSON data retrieval.'):
        systems = get_systems(user, passwd)

    for system in filter_systems(systems, args):
        print(system['id'])