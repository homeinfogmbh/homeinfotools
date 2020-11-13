"""Common constants."""

from urllib.parse import urljoin


__all__ = ['DEPLOYMENTS_URL', 'FINALIZE_URL', 'SYSTEMS_URL', 'VPN_URL']


BASE_URL = 'https://termgr.homeinfo.de'
DEPLOYMENTS_URL = urljoin(BASE_URL, '/list/deployments')
FINALIZE_URL = urljoin(BASE_URL, '/setup/finalize')
SYSTEMS_URL = urljoin(BASE_URL, '/list/systems')
VPN_URL = urljoin(BASE_URL, '/setup/openvpn')
