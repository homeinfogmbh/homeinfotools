"""Common exceptions."""

from subprocess import CompletedProcess


__all__ = [
    'OfflineError',
    'PacmanError',
    'UnknownError',
    'get_exception'
]


class OfflineError(Exception):
    """Indicates that the system is offline."""


class PacmanError(Exception):
    """Indicates an error with pacman."""


class UnknownError(Exception):
    """Indicates an unknown error."""

    def __init__(self, completed_process: CompletedProcess):
        """Creates an exception from the given completed process."""
        super().__init__(completed_process)
        self.completed_process = completed_process

    def __getattr__(self, attribute):
        """Delegates to completed_process."""
        return getattr(self.completed_process, attribute)

    def __str__(self):
        """Returns a string representation of the error."""
        items = []

        if stdout := self.stdout is not None:
            try:
                stdout = stdout.decode()
            except UnicodeDecodeError:
                stdout = str(stdout)

            items.append(f'STDOUT: {stdout}')

        if stderr := self.stderr is not None:
            try:
                stderr = stderr.decode()
            except UnicodeDecodeError:
                stderr = str(stderr)

            items.append(f'STDERR: {stderr}')

        items.append(f'EXIT_CODE: {self.returncode}')
        return ' / '.join(items)


BY_RETURNCODE = {
    255: OfflineError,
    126: IOError,
    1: PacmanError
}


def get_exception(completed_process: CompletedProcess) -> Exception:
    """Raises an exception by the given
    the success status and return code.
    """

    try:
        exception = BY_RETURNCODE[completed_process.returncode]
    except KeyError:
        return UnknownError(completed_process)

    return exception()
