"""Query systems."""

from argparse import Namespace
from datetime import datetime, timedelta
from functools import partial
from json import dump, load
from typing import Iterable

from homeinfotools.his import update_credentials, HISSession
from homeinfotools.logging import LOGGER
from homeinfotools.termgr import SYSTEMS_URL


__all__ = ['get_systems', 'filter_systems']


def query_systems(account: str, passwd: str) -> list:
    """Query systems."""

    LOGGER.debug('Querying systems.')

    with HISSession(account, passwd) as session:
        return session.get_json(SYSTEMS_URL)


def cache_systems(systems: list, args: Namespace) -> list:
    """Caches the systems and returns them."""

    cache = {'timestamp': datetime.now().isoformat(), 'systems': systems}

    with args.cache_file.open('w') as file:
        dump(cache, file)

    return systems


def systems_from_cache(args: Namespace) -> list:
    """Returns cached systems."""

    if not args.cache_file.exists():
        LOGGER.info('Initializing cache.')
        systems = query_systems(*update_credentials(args.user))
        return cache_systems(systems, args)

    LOGGER.debug('Loading cache.')

    with args.cache_file.open('r') as file:
        cache = load(file)

    if timestamp := cache.get('timestamp'):
        timestamp = datetime.fromisoformat(timestamp)

        if timestamp + timedelta(hours=args.cache_time) > datetime.now():
            return cache['systems']

        LOGGER.info('Cache has expired.')
    else:
        LOGGER.warning('Corrupted cache.')

    return cache_systems(query_systems(*update_credentials(args.user)), args)


def get_systems(args: Namespace) -> list:
    """Returns systems."""

    if args.refresh:
        systems = query_systems(*update_credentials(args.user))
        return cache_systems(systems, args)

    return systems_from_cache(args)


def substr_ic_in(string: str, haystack: Iterable[str]) -> bool:
    """Checks whether the string is a substring of
    any strings in the iterable, ignoring the case.
    """

    if not string:
        return False

    string = string.casefold()
    return any(substring in string for substring in haystack)


# pylint:disable=R0911,R0912
def match_system(system: dict, *, args: Namespace) -> bool:
    """Matches the system to the filters."""

    if args.id:
        if system.get('id') not in args.id:
            return False

    if args.os:
        if system.get('operatingSystem') not in args.os:
            return False

    if args.sn:
        if system.get('serialNumber') not in args.sn:
            return False

    deployment = system.get('deployment') or {}

    if args.deployment:
        if deployment.get('id') not in args.deployment:
            return False

    if args.customer:
        customer = deployment.get('customer') or {}
        company = customer.get('company') or {}

        if cid := customer.get('id'):
            match = str(cid) in args.customer
        else:
            match = False

        match = match or substr_ic_in(company.get('name'), args.customer)
        match = match or substr_ic_in(
            company.get('abbreviation'), args.customer)

        if not match:
            return False

    if args.type:
        if deployment.get('type') not in args.type:
            return False

    address = deployment.get('address') or {}

    if args.street:
        if not substr_ic_in(address.get('street'), args.street):
            return False

    if args.house_number:
        if not substr_ic_in(address.get('houseNumber'), args.house_number):
            return False

    if args.zip_code:
        if not substr_ic_in(address.get('zipCode'), args.zip_code):
            return False

    if args.city:
        if not substr_ic_in(address.get('city'), args.city):
            return False

    return True


def filter_systems(systems: list, args: Namespace) -> Iterable[dict]:
    """Filter systems according to the args."""

    return filter(partial(match_system, args=args), systems)
