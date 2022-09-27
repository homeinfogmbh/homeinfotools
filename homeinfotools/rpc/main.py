"""Terminal batch updating utility."""

from json import dump
from logging import basicConfig
from multiprocessing import Pool, Queue
from random import shuffle

from homeinfotools.functions import get_log_level
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.multiprocessing import consume
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.worker import Worker


__all__ = ['main']


def main() -> int:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.system)

    result = Queue()

    try:
        with Pool(args.processes) as pool:
            pool.map(Worker(result, args), args.system, args.chunk_size)
    except KeyboardInterrupt:
        return 1

    if args.json is not None:
        with args.json.open('w') as file:
            dump(dict(consume(result)), file, indent=2)

    return 0
