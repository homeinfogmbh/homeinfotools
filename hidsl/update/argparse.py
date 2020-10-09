"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from pathlib import Path


__all__ = ['get_args']


def get_args() -> Namespace:
    """Returns parsed CLI arguments."""

    parser = ArgumentParser(description='Batch upgrade systems.')
    parser.add_argument('system', type=int, nargs='+',
                        help='systems to upgrade')
    parser.add_argument('-P', '--processes', type=int, metavar='n',
                        help='amount pf parallel processes')
    parser.add_argument('-t', '--timeout', action='store_true',
                        help='enables pacman download timeouts')
    parser.add_argument('-p', '--package', default=(), nargs='+',
                        metavar='pkg', help='packages to explicitely upgrade')
    parser.add_argument('-o', '--overwrite', default=(), nargs='+',
                        metavar='glob', help='globs of files to overwrite')
    parser.add_argument('-k', '--keyring', action='store_true',
                        help='upgrade the keyring before sysupgrade')
    parser.add_argument('-c', '--cleanup', action='store_true',
                        help='cleanup unneeded packages after upgrade')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='enable verbose logging')
    parser.add_argument('-d', '--debuglevel', type=int, default=0,
                        help='set debug level')
    parser.add_argument('-y', '--yes', action='store_true',
                        help='make pacman assume yes')
    parser.add_argument('-n', '--no-stdin', action='store_true',
                        help='make ssh to not read STDIN')
    parser.add_argument('-j', '--json', type=Path, metavar='file',
                        help='write JSON jobs summary when done')
    parser.add_argument('-l', '--logfile', type=Path, metavar='file',
                        help='write log to the given file')
    return parser.parse_args()
