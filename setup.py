#! /usr/bin/env python3

from setuptools import setup


setup(
    name='hidsl',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    install_requires=['requests'],
    python_requires='>=3.8',
    packages=['hidsl', 'hidsl.query', 'hidsl.rpc', 'hidsl.vpn'],
    scripts=['files/sysquery','files/sysrpc', 'files/sysvpn'],
    license='GPLv3',
    description='HOMEINFO Digital Signage Linux configurator.'
)
