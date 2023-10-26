import logging
import math
from datetime import datetime
from typing import Optional, Union

import pytz
from dateutil.parser import parse
from web3 import Web3
from web3.exceptions import BlockNotFound
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider

logger = logging.getLogger(__name__)


def get_checksum_address(address):
    return Web3.toChecksumAddress(address)


def change_case(str):
    return "".join(["_" + i.lower() if i.isupper() else i for i in str]).lstrip("_")


def round_(x, div_by=18):
    try:
        return round(int(x) / math.pow(10, div_by), div_by)
    except ValueError as e:
        print(x)
        raise e


def to_aware_datetime(timestamp: Union[int, datetime]):
    if isinstance(timestamp, int):
        return datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    elif isinstance(timestamp, datetime):
        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
            return timestamp.replace(tzinfo=pytz.utc)
        return timestamp
    elif isinstance(timestamp, str):
        return to_aware_datetime(parse(timestamp))
    logger.info(f"{timestamp, type(timestamp)}")
    raise ValueError("Invalid timestamp")


def _amount(x, div_by=18):
    return round_(x, div_by)


def get_factor(x):
    return math.pow(10, x)


def to_date_components(expiration_date):
    difference = expiration_date - datetime.now(pytz.utc)
    days = difference.days
    seconds = difference.seconds
    hours = seconds // 3600

    return days, hours


def _price(x):
    return round(round_(x, 8), 2)


def are_addresses_equal(address1: Optional[str] = None, address2: Optional[str] = None):
    def f(address):
        return get_checksum_address(address) if address else address

    return f(address1) == f(address2)


import os


def get_web3():
    provider = HTTPProvider(os.environ.get("RPC"), request_kwargs={"timeout": 10})

    # Remove the default JSON-RPC retry middleware
    # as it correctly cannot handle eth_getLogs block range
    # throttle down.
    provider.middlewares.clear()

    web3 = Web3(provider)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3


def get_account(private_key):
    web3 = get_web3()
    return Web3.toChecksumAddress(
        web3.eth.account.privateKeyToAccount(private_key).address
    )


def get_latest_block(provider):
    block_number = get_web3(provider).eth.blockNumber
    return block_number


def to_wei(x, mul_by=18):
    return x * math.pow(10, mul_by)
