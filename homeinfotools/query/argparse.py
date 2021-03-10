"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from homeinfotools.os import CACHE_DIR


__all__ = ['get_args']


CACHE_FILE = CACHE_DIR / 'sysquery.cache'


def get_args() -> Namespace:
    """Returns parsed CLI arguments."""

    parser = ArgumentParser(description='Retrieve and filter systems.')
    parser.add_argument('-U', '--user', metavar='account',
                        help='the HIS user account')
    parser.add_argument('-i', '--id', nargs='+', type=int, metavar='id',
                        help='filter by system IDs')
    parser.add_argument('-o', '--os', nargs='+', metavar='operating system',
                        help='filter by operating systems')
    parser.add_argument('--sn', nargs='+', metavar='serial number',
                        help='filter by serial numbers')
    parser.add_argument('-D', '--deployment', nargs='+', type=int,
                        metavar='deployment', help='filter by deployments')
    parser.add_argument('-C', '--customer', nargs='+', type=str.casefold,
                        metavar='customer', help='filter by customers')
    parser.add_argument('-t', '--type', nargs='+', metavar='type',
                        help='filter by types')
    parser.add_argument('-s', '--street', nargs='+', type=str.casefold,
                        metavar='street', help='filter by streets')
    parser.add_argument('-H', '--house-number', nargs='+', type=str.casefold,
                        metavar='house number', help='filter by house numbers')
    parser.add_argument('-z', '--zip-code', nargs='+', type=str.casefold,
                        metavar='zip code', help='filter by zip codes')
    parser.add_argument('-c', '--city', nargs='+', type=str.casefold,
                        metavar='city', help='filter by cities')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose mode')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('-f', '--refresh', action='store_true',
                        help='force refreshing of cache')
    parser.add_argument('--cache-file', type=Path, default=CACHE_FILE,
                        metavar='file', help='use the given file as cache')
    parser.add_argument('--cache-time', type=int, default=24, metavar='hours',
                        help='sets the caching time in hours')
    return parser.parse_args()
