"""Common exceptions."""

from subprocess import CompletedProcess


__all__ = ['RemoteProcessError', 'SSHConnectionError']


class RemoteProcessError(Exception):
    """Error when executing processes on remote systems."""

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

        if stdout := self.stdout:
            items.append(f'STDOUT: {stdout}')

        if stderr := self.stderr:
            items.append(f'STDERR: {stderr}')

        items.append(f'EXIT_CODE: {self.returncode}')
        return ' / '.join(items)


class SSHConnectionError(RemoteProcessError):
    """Indicates that the SSH could not connect to the system."""
