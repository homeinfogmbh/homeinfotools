"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from multiprocessing import cpu_count
from pathlib import Path


__all__ = ['get_args']


def get_args() -> Namespace:
    """Returns parsed CLI arguments."""

    parser = ArgumentParser(description='Transfer files from and to systems.')
    parser.add_argument(
        'system', type=int, nargs='+', help='systems to upgrade'
    )
    parser.add_argument(
        '-S', '--send', action='store_true',
        help='send a file to the system(s)'
    )
    parser.add_argument(
        '-R', '--retrieve', action='store_true',
        help='retrieve a file from the system(s)'
    )
    parser.add_argument('src', type=Path, help='the source file')
    parser.add_argument('dst', type=Path, help='the destination file')
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable debug logging'
    )
    parser.add_argument(
        '-p', '--processes', type=int, metavar='n', default=cpu_count(),
        help='amount of parallel processes'
    )
    parser.add_argument(
        '-s', '--shuffle', action='store_true', help='shuffle systems'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='enable verbose logging'
    )
    args = parser.parse_args()

    if sum((args.send, args.retrieve)) != 1:
        parser.error('Must specify either send xor receive.')

    return args
