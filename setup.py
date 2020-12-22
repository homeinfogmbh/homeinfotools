#! /usr/bin/env python3
"""Installation script."""

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
        'homeinfotools.his',
        'homeinfotools.query',
        'homeinfotools.rpc',
        'homeinfotools.vpn'
    ],
    entry_points={
        'console_scripts': [
            'sysquery = homeinfotools.query.main:main',
            'sysrpc = homeinfotools.rpc.main:main',
            'sysvpn = homeinfotools.vpn.main:main',
        ],
    },
    license='GPLv3',
    description='Tools to manage HOMEINFO digital signge systems.'
)
