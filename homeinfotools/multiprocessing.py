"""Multiprocessing worker."""

from argparse import Namespace
from datetime import datetime
from logging import INFO, Logger, getLogger
from multiprocessing import Process, Queue
from queue import Empty
from signal import SIGUSR1, SIGUSR2, signal
from typing import Any, Iterator, Sequence, Type

from setproctitle import setproctitle

from homeinfotools.exceptions import SSHConnectionError
from homeinfotools.logging import syslogger


__all__ = ['BaseWorker', 'multiprocess']


class BaseWorker:
    """Stored args and manager to process systems."""

    __slots__ = ('index', 'systems', 'results', 'running', 'current_system')

    def __init__(self, index: int, systems: Queue, results: Queue):
        """Sets the command line arguments."""
        self.index = index
        self.systems = systems
        self.results = results
        self.running = True
        self.current_system = None

    def __call__(self, args: Namespace) -> None:
        """Runs the worker on the given system."""
        setproctitle(self.name)
        signal(SIGUSR1, self.signal)
        signal(SIGUSR2, self.signal)

        while self.running:
            try:
                self.current_system = system = self.systems.get(timeout=1)
            except Empty:
                self.logger.info('Finished')
                return

            result = self.process_system(system, args)
            self.results.put_nowait((system, result))

        self.logger.info('Aborted')

    @property
    def info(self) -> str:
        """Returns information about the state of the worker."""
        if self.current_system is None:
            return 'idle'

        return f'Processing system #{self.current_system}'

    @property
    def logger(self) -> Logger:
        """Returns the worker's logger."""
        logger = getLogger(self.name)
        logger.setLevel(INFO)
        return logger

    @property
    def name(self) -> str:
        """Returns the worker's name."""
        return f'hidsltools-worker-{self.index}'

    def signal(self, signal_number: int, _: Any) -> None:
        """Handles the given signal."""
        if signal_number == SIGUSR1:
            self.logger.info(self.info)
        elif signal_number == SIGUSR2:
            self.running = False
        else:
            self.logger.error('Received invalid signal: %i', signal_number)

    def process_system(self, system: int, args: Namespace) -> dict:
        """Processes a single system."""
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

    wait_for_processes(list(spawn_workers(
        worker_cls,
        processes,
        sequence_to_queue(systems),
        results := Queue(),
        args
    )))
    return dict(iter_queue(results))


def sequence_to_queue(sequence: Sequence[Any]) -> Queue:
    """Returns a queue with items from the given sequence."""

    queue = Queue(len(sequence))

    for item in sequence:
        queue.put(item)

    return queue


def spawn_workers(
        worker_cls: Type[BaseWorker],
        amount: int,
        systems: Queue,
        results: Queue,
        args: Namespace
) -> Iterator[Process]:
    """Spawns worker processes."""

    for index in range(amount):
        worker = worker_cls(index, systems, results)
        process = Process(target=worker, args=(args,))
        process.start()
        yield process


def wait_for_processes(processes: list[Process]) -> None:
    """Wait for the given processes."""

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.kill()

        raise


def iter_queue(queue: Queue) -> Iterator[Any]:
    """Yield queue items."""

    while not queue.empty():
        yield queue.get()
