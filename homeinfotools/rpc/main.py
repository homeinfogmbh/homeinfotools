"""Terminal backtch updating utility."""

from json import dump
from logging import basicConfig
from multiprocessing import Manager, Pool

from homeinfotools.logging import LOG_FORMAT
from homeinfotools.rpc.argparse import get_args
from homeinfotools.rpc.json import to_json
from homeinfotools.rpc.functions import get_log_level
from homeinfotools.rpc.processing import Worker


__all__ = ['main']


def run(manager: Manager):
    """Runs the program with a manager."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=get_log_level(args))
    jobs = {system: manager.dict() for system in args.system}
    worker = Worker(args, jobs)

    with Pool(processes=args.processes) as pool:
        pool.map(worker, args.system)

    if args.json is not None:
        json = {system: to_json(job) for system, job in jobs.items()}

        with args.json.open('w') as file:
            dump(json, file, indent=2)


def main():
    """Runs the script."""


    with Manager() as manager:
        run(manager)
