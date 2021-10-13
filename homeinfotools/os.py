"""Operating system-specific implementations."""

from os import getenv, name
from pathlib import Path


__all__ = ['SSH', 'RSYNC', 'CACHE_DIR']


if name == 'posix':
    SSH = '/usr/bin/ssh'
    RSYNC = '/usr/bin/rsync'
    CACHE_DIR = Path.home() / '.cache'
elif name == 'nt':
    SSH = 'ssh'
    RSYNC = 'rsync'
    CACHE_DIR = Path(getenv('TEMP') or getenv('TMP'))
else:
    raise NotImplementedError('Unsupported operating system.')
