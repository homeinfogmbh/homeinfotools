"""Terminal batch updating utility."""

from json import dump
from logging import basicConfig
from random import shuffle

from homeinfotools.functions import get_log_level, handle_keyboard_interrupt
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.multiprocessing import multiprocess
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.worker import Worker


__all__ = ['main']


@handle_keyboard_interrupt
def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.systems)

    result = multiprocess(Worker, args.system, args.processes, args=args)

    if args.json is not None:
        with args.json.open('w') as file:
            dump(dict(result), file, indent=2)
