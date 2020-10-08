#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='hids-scripts',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    requires=['requests'],
    packages=['hidsl', 'hidsl.update', 'hidsl.vpn'],
    scripts=['files/sysvpn', 'files/termupd'],
    description='HOMEINFO Digital Signage Linux configurator.'
)
