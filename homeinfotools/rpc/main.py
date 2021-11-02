"""Terminal batch updating utility."""

from json import dump
from logging import basicConfig
from multiprocessing import Pool

from homeinfotools.functions import get_log_level
from homeinfotools.logging import LOGGER, LOG_FORMAT
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.worker import Worker


__all__ = ['main']


def run() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))

    with Pool(processes=args.processes) as pool:
        result = pool.map(Worker(args), args.system)

    if args.json is not None:
        with args.json.open('w') as file:
            dump(dict(result), file, indent=2)


def main() -> int:
    """Main script with guard."""

    try:
        run()
    except KeyboardInterrupt:
        LOGGER.error('Aborted by user.')
        return 1

    return 0
