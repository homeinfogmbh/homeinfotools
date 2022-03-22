"""Batch sync files."""

from logging import basicConfig
from random import shuffle

from homeinfotools.functions import get_log_level, handle_keyboard_interrupt
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.multiprocessing import multiprocess
from homeinfotools.filetransfer.argparse import get_args
from homeinfotools.filetransfer.worker import Worker


__all__ = ['main']


@handle_keyboard_interrupt
def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    if args.shuffle:
        shuffle(args.systems)

    multiprocess(Worker, args.system, args.processes, args=args)
