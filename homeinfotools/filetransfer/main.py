"""Batch sync files."""

from logging import basicConfig
from multiprocessing import Manager, Pool
from random import shuffle

from homeinfotools.functions import get_log_level
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.filetransfer.argparse import get_args
from homeinfotools.filetransfer.worker import Worker


__all__ = ['main']


def main() -> int:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.system)

    results = Manager().dict()

    try:
        with Pool(args.processes) as pool:
            pool.map(
                Worker(args, results), args.system, chunksize=args.chunk_size
            )
    except KeyboardInterrupt:
        return 1

    return 0
