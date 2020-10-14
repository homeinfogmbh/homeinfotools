"""Terminal backtch updating utility."""

from json import dump
from logging import basicConfig
from multiprocessing import Manager, Pool

from hidsl.logging import LOG_FORMAT
from hidsl.rpc.argparse import get_args
from hidsl.rpc.json import to_json
from hidsl.rpc.functions import get_log_level
from hidsl.rpc.processing import Worker


__all__ = ['main']


def run(manager: Manager):
    """Runs the program with a manager."""

    args = get_args()
    loglevel = get_log_level(args)
    basicConfig(format=LOG_FORMAT, level=loglevel)
    worker = Worker(args, manager)
    jobs = {}

    with Pool(processes=args.processes) as pool:
        for system, job in pool.imap_unordered(worker, args.system):
            jobs[system] = dict(job)

    if args.json is not None:
        json = {system: to_json(job) for system, job in jobs.items()}

        with args.json.open('w') as file:
            dump(json, file, indent=2)


def main():
    """Runs the script."""

    with Manager() as manager:
        run(manager)
