"""Common constants."""

from logging import getLogger
from pathlib import Path
from sys import argv


__all__ = ['LOG_FORMAT', 'LOGGER']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger(Path(argv[0]).name)
