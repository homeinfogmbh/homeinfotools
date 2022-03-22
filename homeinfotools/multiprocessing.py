"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime
from multiprocessing import Process, Queue
from queue import Empty
from typing import Any, Iterator, Type

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker', 'multiprocess']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('index', 'args', 'systems', 'results')

    def __init__(self, index: int, systems: Queue, results: Queue):
        """Sets the command line arguments."""
        self.index = index
        self.systems = systems
        self.results = results

    def __call__(self, args: Namespace) -> None:
        """Runs the worker on the given system."""
        self.update_process_title()

        while True:
            try:
                system = self.systems.get_nowait()
            except Empty:
                return

            result = self.process_system(system, args)
            self.results.put_nowait((system, result))

    def update_process_title(self, system: int | None = None) -> None:
        """Returns the current process title."""
        if system is None:
            return setproctitle(f'hidsltools-worker-{self.index}')

        return setproctitle(f'hidsltools-worker-{self.index}@{system}')

    def process_system(self, system: int, args: Namespace) -> dict:
        """Processes a single system."""
        self.update_process_title(system)
        result = {'start': (start := datetime.now()).isoformat()}

        try:
            result['result'] = self.run(system, args)
        except SSHConnectionError:
            syslogger(system).error('Could not establish SSH connection.')
            result['success'] = False
        else:
            result['success'] = True

        result['end'] = (end := datetime.now()).isoformat()
        result['duration'] = str(end - start)
        return result

    @staticmethod
    def run(system: int, args: Namespace) -> dict:
        """Runs the respective processes."""
        raise NotImplementedError()


def multiprocess(
        worker_cls: Type[BaseWorker],
        systems: list[int],
        processes: int,
        args: Namespace
) -> dict:
    """Spawns workers and waits for them to finish."""

    systems_queue = Queue(len(systems))
    results = Queue()

    for system in systems:
        systems_queue.put_nowait(system)

    proc_list = []

    for index in range(processes):
        target = worker_cls(index, systems_queue, results)
        process = Process(target=target, args=(args,))
        proc_list.append(process)
        process.start()

    for process in proc_list:
        process.join()

    return dict(iter_queue(results))


def iter_queue(queue: Queue) -> Iterator[Any]:
    """Returns queue elements as dict."""

    while not queue.empty():
        yield queue.get_nowait()
