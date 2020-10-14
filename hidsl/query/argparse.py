"""Argument parsing."""

from argparse import ArgumentParser, Namespace


__all__ = ['get_args']


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
    parser.add_argument('-C', '--customer', nargs='+', metavar='customer',
                        help='filter by customers')
    parser.add_argument('-t', '--type', nargs='+', metavar='type',
                        help='filter by types')
    parser.add_argument('-s', '--street', nargs='+', metavar='street',
                        help='filter by streets')
    parser.add_argument('-n', '--house-number', nargs='+',
                        metavar='house number', help='filter by house numbers')
    parser.add_argument('-z', '--zip-code', nargs='+', metavar='zip code',
                        help='filter by zip codes')
    parser.add_argument('-c', '--city', nargs='+', metavar='city',
                        help='filter by cities')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose mode')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode')
    return parser.parse_args()
