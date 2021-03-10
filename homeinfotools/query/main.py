"""Main script."""

from logging import DEBUG, INFO, WARNING, basicConfig

from homeinfotools.his import ErrorHandler
from homeinfotools.logging import LOG_FORMAT, LOGGER
from homeinfotools.query.argparse import get_args
from homeinfotools.query.functions import filter_systems, get_systems


__all__ = ['main']


def main():
    """Runs the script."""

    args = get_args()
    loglevel = DEBUG if args.debug else INFO if args.verbose else WARNING
    basicConfig(format=LOG_FORMAT, level=loglevel)
    LOGGER.info('Retrieving systems.')

    with ErrorHandler('Error during JSON data retrieval.'):
        systems = get_systems(args)

    for system in filter_systems(systems, args):
        print(system.get('id'))
