"""Common constants."""

from logging import getLogger
from pathlib import Path
from sys import argv


__all__ = ['LOG_FORMAT', 'LOGGER', 'syslogger']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger(Path(argv[0]).name)


def syslogger(system: int):
    """Returns a sub-logger for the given system."""

    return LOGGER.getChild(str(system))
