#! /usr/bin/env python3
"""Installation script."""

from pathlib import Path
from setuptools import setup


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
        'homeinfotools.query',
        'homeinfotools.rpc',
        'homeinfotools.vpn'
    ],
    scripts=[str(path) for path in Path('scripts').iterdir()],
    license='GPLv3',
    description='HOMEINFO Digital Signage Linux configurator.'
)
