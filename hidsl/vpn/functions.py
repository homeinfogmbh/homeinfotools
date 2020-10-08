"""Common functions."""

from pathlib import Path
from sys import exit, stdout    # pylint: disable=W0622

from requests import session

from hidsl.logging import LOGGER
from hidsl.vpn.common import HIS_LOGIN_URL, TERMGR_VPN_URL


__all__ = ['retrieve_data']


def retrieve_data(login_data: dict, vpn_data: dict, path: Path):
    """Retrieves OpenVPN data for the respective system."""

    with session() as sess:
        response = sess.post(HIS_LOGIN_URL, json=login_data)

        if response.status_code != 200:
            LOGGER.error('Error during login.')
            LOGGER.debug(response.content)
            exit(2)

        response = sess.post(TERMGR_VPN_URL, json=vpn_data)

        if response.status_code != 200:
            LOGGER.error('Error during VPN data retrieval.')
            LOGGER.debug(response.content)
            exit(3)

        if path:
            with path.open('wb') as file:
                file.write(response.content)
        else:
            stdout.buffer.write(response.content)
