"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from pathlib import Path


__all__ = ['get_args']


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description='OpenVPN configuration retrieval.')
    parser.add_argument('-u', '--user', help='HIS user name')
    parser.add_argument('-w', '--windows', action='store_true',
                        help='package for MS Windows systems')
    parser.add_argument('-o', '-f', '--file', type=Path, help='output file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('system', type=int, help='the system ID')
    return parser.parse_args()
