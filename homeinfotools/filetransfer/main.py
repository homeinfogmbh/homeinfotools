"""Batch sync files."""

from logging import basicConfig
from random import shuffle

from homeinfotools.functions import get_log_level
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.multiprocessing import multiprocess
from homeinfotools.filetransfer.argparse import get_args
from homeinfotools.filetransfer.worker import Worker


__all__ = ['main']


def main() -> int:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.system)

    try:
        multiprocess(Worker, args.system, args.processes, args=args)
    except KeyboardInterrupt:
        return 1

    return 0
