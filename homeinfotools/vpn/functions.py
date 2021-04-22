"""Common functions."""

from argparse import Namespace

from homeinfotools.his import DownloadError, HISSession
from homeinfotools.logging import LOGGER
from homeinfotools.termgr import FINALIZE_URL, VPN_URL


__all__ = ['configure']


def get_vpn_data(session: HISSession, system: int, windows: bool) -> bytes:
    """Retrieves OpenVPN data for the respective system."""

    json = {'system': system, 'windows': windows}
    response = session.post(VPN_URL, json=json)

    if response.status_code != 200:
        raise DownloadError(response)

    return response.content


def finalize_system(session: HISSession, system: int, *, serial_number: str,
                    operating_system: str, model: str, pubkey: str) -> bool:
    """Finalizes the system."""

    json = {'system': system}

    if serial_number is not None:
        json['sn'] = serial_number

    if operating_system is not None:
        json['os'] = operating_system

    if model is not None:
        json['model'] = model

    if pubkey is not None:
        json['wg_pubkey'] = pubkey

    response = session.post(FINALIZE_URL, json=json)

    if response.status_code != 200:
        LOGGER.error('Could not finalize system.')
        LOGGER.debug(response.content)
        return False

    return True


def configure(user: str, passwd: str, args: Namespace) -> bytes:
    """Retrieves OpenVPN data for the respective system."""

    with HISSession(user, passwd) as session:
        vpn_data = get_vpn_data(session, args.system, args.windows)
        finalize_system(
            session, args.system, serial_number=args.serial_number,
            operating_system=args.operating_system, model=args.model,
            pubkey=args.pubkey)
        return vpn_data
