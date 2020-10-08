"""Terminal backtch updating utility."""

from functools import partial
from json import dump
from logging import DEBUG, INFO, WARN, basicConfig
from multiprocessing import Manager, Pool
from os import getpid, linesep
from signal import SIGUSR1, SIGUSR2, signal

from hidsl.logging import LOG_FORMAT, LOGGER
from hidsl.update.argparse import get_args
from hidsl.update.functions import get_header
from hidsl.update.functions import print_finished
from hidsl.update.functions import print_pending
from hidsl.update.functions import upgrade
from hidsl.update.proxy import UpdateJobProxy


__all__ = ['main']


def main():
    """Runs the script."""

    args = get_args()
    manager = Manager()
    jobs = manager.dict()

    # Polulate manage dicts for systems.
    for system in args.system:
        jobs[system] = manager.dict()

    signal(SIGUSR1, lambda signum, frame: print_finished(jobs, args.system))
    signal(SIGUSR2, lambda signum, frame: print_pending(jobs, args.system))
    loglevel = DEBUG if args.debug else INFO if args.verbose else WARN
    basicConfig(format=LOG_FORMAT, level=loglevel)
    proc_func = partial(upgrade, args=args, jobs=jobs)
    LOGGER.info('PID: %s', getpid())

    # Initialize log file.
    if args.logfile is not None:
        with args.logfile.open('w') as logfile:
            logfile.writelines(linesep.join(get_header()) + linesep)

    with Pool(processes=args.processes) as pool:
        pool.map(proc_func, args.system)

    if args.json is not None:
        json = {system: UpdateJobProxy(jobs[system]).to_json() for system in jobs}

        with args.json.open('w') as file:
            dump(json, file, indent=2)
