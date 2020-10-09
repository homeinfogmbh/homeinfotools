"""Common functions."""

from getpass import getpass
from sys import exit    # pylint: disable=W0622
from typing import Tuple

from requests import session

from hidsl.logging import LOGGER
from hidsl.vpn.common import HIS_LOGIN_URL, TERMGR_VPN_URL
from hidsl.vpn.exceptions import DownloadError, LoginError


__all__ = ['read_credentials', 'get_vpn_data']


def read_credentials(user: str) -> Tuple[str, str]:
    """Reads the credentials for a HIS account."""

    if not user:
        try:
            user = input('User name: ')
        except (EOFError, KeyboardInterrupt):
            print()
            LOGGER.error('Aborted by user.')
            exit(1)

    try:
        passwd = getpass('Password: ')
    except (EOFError, KeyboardInterrupt):
        print()
        LOGGER.error('Aborted by user.')
        exit(1)

    return (user, passwd)


def get_data(sess: session, login_data: dict, vpn_data: dict) -> bytes:
    """Retrieves OpenVPN data from for the respective system."""

    response = sess.post(HIS_LOGIN_URL, json=login_data)

    if response.status_code != 200:
        raise LoginError(response)

    response = sess.post(TERMGR_VPN_URL, json=vpn_data)

    if response.status_code != 200:
        raise DownloadError(response)

    return response.content


def get_vpn_data(user: str, passwd: str, system: int, windows: bool) -> bytes:
    """Retrieves OpenVPN data for the respective system."""

    login_data = {'account': user, 'passwd': passwd}
    vpn_data = {'system': system, 'windows': windows}

    with session() as sess:
        return get_data(sess, login_data, vpn_data)
