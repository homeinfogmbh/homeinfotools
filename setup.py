#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='hidsl-scripts',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    requires=['requests'],
    packages=['hidsl', 'hidsl.query', 'hidsl.rpc', 'hidsl.vpn'],
    scripts=['files/sysquery','files/sysrpc', 'files/sysvpn'],
    description='HOMEINFO Digital Signage Linux configurator.'
)
