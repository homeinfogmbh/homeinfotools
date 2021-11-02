"""Batch sync files."""

from logging import basicConfig
from multiprocessing import Pool

from homeinfotools.functions import get_log_level, handle_keyboard_interrupt
from homeinfotools.logging import LOG_FORMAT
from homeinfotools.filetransfer.argparse import get_args
from homeinfotools.filetransfer.worker import Worker


__all__ = ['main']


@handle_keyboard_interrupt
def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    with Pool(processes=args.processes) as pool:
        pool.map(Worker(args), args.system)
