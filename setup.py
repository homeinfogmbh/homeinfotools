#! /usr/bin/env python3
"""Installation script."""

from os import name
from pathlib import Path
from setuptools import setup


SCRIPTS = Path('scripts').iterdir()

if name == 'nt':
    SCRIPTS = [path.rename(f'{path}.py') for path in SCRIPTS]


setup(
    name='homeinfotools',
    version_format='{tag}',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    python_requires='>=3.8',
    install_requires=['setuptools-git-version', 'requests'],
    packages=[
        'homeinfotools',
        'homeinfotools.his',
        'homeinfotools.query',
        'homeinfotools.rpc',
        'homeinfotools.vpn'
    ],
    scripts=[str(path) for path in SCRIPTS],
    license='GPLv3',
    description='Tools to manage HOMEINFO digital signge systems.'
)
