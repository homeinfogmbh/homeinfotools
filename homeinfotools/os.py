"""Operating system-specific implementations."""

from os import getenv, name
from pathlib import Path


__all__ = ['SSH', 'CACHE_DIR']


if name == 'posix':
    SSH = '/usr/bin/ssh'
    CACHE_DIR = Path.home() / '.cache'
elif name == 'nt':
    SSH = 'ssh'
    CACHE_DIR = Path(getenv('TEMP') or getenv('TMP'))
else:
    raise NotImplementedError('Unsupported operating system.')
