"""Multiprocessing worker."""

from argparse import Namespace
from collections import defaultdict
from datetime import datetime
from itertools import chain
from multiprocessing import Process, Queue
from queue import Empty
from typing import Type

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker', 'multiprocess']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('index', 'args', 'systems', 'results')

    def __init__(self, index: int, args: Namespace, systems: Queue[int]):
        """Sets the command line arguments."""
        self.index = index
        self.args = args
        self.systems = systems
        self.results = defaultdict(dict)

    def __call__(self) -> None:
        """Runs the worker on the given system."""
        setproctitle(f'hidsltools-worker-{self.index}')

        while True:
            try:
                system = self.systems.get_nowait()
            except Empty:
                return

            self._process_system(system, self.results[system])

    def _process_system(self, system: int, result: dict) -> None:
        """Processes a single system."""
        result['start'] = (start := datetime.now()).isoformat()

        try:
            result['result'] = self.run(system)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')
            result['success'] = False
        else:
            result['success'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)

    def run(self, system: int) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()


def multiprocess(worker_cls: Type[BaseWorker], args: Namespace) -> dict:
    """Spawns workers and waits for them to finish."""

    systems = Queue(len(args.system))

    for system in args.system:
        systems.put_nowait(system)

    workers = []
    processes = []

    for index in range(args.processes):
        process = Process(target=(worker := worker_cls(index, args, systems)))
        workers.append(worker)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return dict(chain.from_iterable(
        worker.results.items() for worker in workers
    ))
