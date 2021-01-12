#! /usr/bin/env python3
"""Installation script."""

from setuptools import setup


setup(
    name='homeinfotools',
    use_scm_version=True,
    setup_requires=['requests', 'setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    python_requires='>=3.8',
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
    url='https://github.com/homeinfogmbh/homeinfotools',
    license='GPLv3',
    description='Tools to manage HOMEINFO digital signge systems.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords='python HOMEINFO systems client'
)
