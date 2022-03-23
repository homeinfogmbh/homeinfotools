"""Common functions."""

from argparse import Namespace
from functools import wraps
from logging import DEBUG, INFO, WARNING
from subprocess import DEVNULL, PIPE, run, CompletedProcess
from typing import Callable, Iterable

from homeinfotools.logging import LOGGER


__all__ = [
    'completed_process_to_json',
    'execute',
    'get_log_level',
    'handle_keyboard_interrupt'
]


def completed_process_to_json(completed_process: CompletedProcess) -> dict:
    """Converts a completed process into a JSON-ish dict."""

    return {
        'args': completed_process.args,
        'returncode': completed_process.returncode,
        'stdout': completed_process.stdout,
        'stderr': completed_process.stderr,
    }


def execute(
        command: str | Iterable[str],
        *,
        timeout: int | None = None
) -> CompletedProcess:
    """Executes the given command."""

    return run(
        command, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, text=True,
        check=False, timeout=timeout
    )


def get_log_level(args: Namespace) -> int:
    """Returns the set logging level."""

    return DEBUG if args.debug else INFO if args.verbose else WARNING


def handle_keyboard_interrupt(
        function: Callable[..., None]
) -> Callable[..., int]:
    """Decorator to run a function with handled keyboard interrupt."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> int:
        try:
            return_code = function(*args, **kwargs)
        except KeyboardInterrupt:
            LOGGER.error('Aborted by user.')
            return 1

        return 0 if return_code is None else return_code

    return wrapper
