"""Common functions."""

from hidsl.his import DownloadError, HISSession
from hidsl.termgr import VPN_URL


__all__ = ['get_vpn_data']


def get_vpn_data(user: str, passwd: str, system: int, windows: bool) -> bytes:
    """Retrieves OpenVPN data for the respective system."""

    json = {'system': system, 'windows': windows}

    with HISSession(user, passwd) as session:
        response = session.post(VPN_URL, json=json)

        if response.status_code != 200:
            raise DownloadError(response)

        return response.content
