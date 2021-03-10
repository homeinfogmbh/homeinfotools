"""Terminal backtch updating utility."""

from json import dump
from logging import basicConfig
from multiprocessing import Pool

from homeinfotools.logging import LOG_FORMAT
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.functions import get_log_level
from homeinfotools.rpc.processing import Worker


__all__ = ['main']


def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    with Pool(processes=args.processes) as pool:
        result = pool.map(Worker(args), args.system)

    if args.json is not None:
        with args.json.open('w') as file:
            dump(dict(result), file, indent=2)
