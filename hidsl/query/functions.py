"""Query systems."""

from argparse import Namespace
from datetime import datetime, timedelta
from functools import partial
from json import dump, load
from typing import Iterable

from hidsl.his import update_credentials, HISSession
from hidsl.logging import LOGGER
from hidsl.termgr import SYSTEMS_URL


__all__ = ['get_systems', 'filter_systems']


def query_systems(account: str, passwd: str) -> list:
    """Query systems."""

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

    if args.cache_file.exists():
        LOGGER.debug('Loading cache.')

        with args.cache_file.open('r') as file:
            cache = load(file)
    else:
        LOGGER.debug('Cache does not exist.')
        cache = {}

    if timestamp := cache.get('timestamp'):
        timestamp = datetime.fromisoformat(timestamp)

        if timestamp + timedelta(hours=args.cache_time) > datetime.now():
            return cache['systems']

        LOGGER.info('Cache has expired.')

    return cache_systems(query_systems(*update_credentials(args.user)), args)


def get_systems(args: Namespace) -> list:
    """Returns systems."""

    if args.no_caching or args.force:
        systems = query_systems(*update_credentials(args.user))

    if args.no_caching:
        return systems

    if args.force:
        return cache_systems(systems, args)

    return systems_from_cache(args)



# pylint:disable=R0911,R0912
def match_system(system: dict, *, args: Namespace) -> bool:
    """Matches the system to the filters."""

    if args.id is not None:
        if system.get('id') not in args.id:
            return False

    if args.os is not None:
        if system.get('operatingSystem') not in args.os:
            return False

    if args.sn is not None:
        if system.get('serialNumber') not in args.sn:
            return False

    deployment = system.get('deployment') or {}

    if args.deployment is not None:
        if deployment.get('id') not in args.deployment:
            return False

    if args.customer is not None:
        customer = deployment.get('customer') or {}
        company = customer.get('company') or {}
        match = str(customer['id']) in args.customer
        match = match or company.get('name') in args.customer
        match = match or company.get('abbreviation') in args.customer

        if not match:
            return False

    if args.type is not None:
        if deployment.get('type') not in args.type:
            return False

    address = deployment.get('address') or {}

    if args.street is not None:
        if address.get('street') not in args.street:
            return False

    if args.house_number is not None:
        if address.get('houseNumber') not in args.house_number:
            return False

    if args.zip_code is not None:
        if address.get('zipCode') not in args.zip_code:
            return False

    if args.city is not None:
        if address.get('city') not in args.city:
            return False

    return True


def filter_systems(systems: list, args: Namespace) -> Iterable[dict]:
    """Filter systems according to the args."""

    return filter(partial(match_system, args=args), systems)
