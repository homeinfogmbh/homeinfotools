#! /usr/bin/env python3

from os import name
from pathlib import Path
from setuptools import setup


SCRIPTS = Path('scripts').iterdir()

if os.name == 'nt':
    SCRIPTS = [script.rename(f'{script}.py') for script in SCRIPTS]


setup(
    name='homeinfotools',
    version_format='{tag}',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    python_requires='>=3.8',
    setup_requires=['setuptools-git-version'],
    install_requires=['requests'],
    packages=[
        'homeinfotools',
        'homeinfotools.query',
        'homeinfotools.rpc',
        'homeinfotools.vpn'
    ],
    scripts=[str(path) for path in SCRIPTS],
    license='GPLv3',
    description='HOMEINFO Digital Signage Linux configurator.'
)
