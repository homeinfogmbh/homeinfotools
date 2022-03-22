"""Terminal batch updating utility."""

from json import dump
from logging import basicConfig
from random import shuffle

from homeinfotools.functions import get_log_level
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.multiprocessing import multiprocess
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.worker import Worker


__all__ = ['main']


def main() -> int:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.system)

    try:
        result = multiprocess(Worker, args.system, args.processes, args=args)
    except KeyboardInterrupt:
        return 1

    if args.json is not None:
        with args.json.open('w') as file:
            dump(dict(result), file, indent=2)

    return 0
