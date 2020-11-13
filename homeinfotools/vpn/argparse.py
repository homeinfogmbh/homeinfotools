"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from pathlib import Path


__all__ = ['get_args']


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description='OpenVPN configuration retrieval.')
    parser.add_argument('system', type=int, help='the system ID')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('-f', '--file', type=Path, help='output file')
    parser.add_argument('-m', '--model', help='Set model')
    parser.add_argument('-o', '--operating-system', help='Set OS')
    parser.add_argument('-p', '--pubkey', help='Set WireGuard pubkey')
    parser.add_argument('-s', '--serial-number', help='Set serial number')
    parser.add_argument('-u', '--user', help='HIS user name')
    parser.add_argument('-w', '--windows', action='store_true',
                        help='package for MS Windows systems')
    return parser.parse_args()
