# Contract Registry
import importlib
import logging
from collections import defaultdict
from typing import Any

from pipe import groupby, select, where
from services.web3_service import get_contract_instance
from utility import get_web3
from web3 import Web3

logger = logging.getLogger(__name__)

ContractRegistryMap: Any = defaultdict(lambda: defaultdict(dict))


def get_checksum_address(address):
    return Web3.toChecksumAddress(address)


def get(contract_address, environment, abi_path=None, index=None):
    return get_contract_instance(
        index=index,
        contract_address=get_checksum_address(contract_address),
        environment=environment,
        abi_path=abi_path,
    )


def register(
    contract_address,
    environment,
    abi_path,
):

    contract_instance = get_contract_instance(
        contract_address=get_checksum_address(contract_address),
        environment=environment,
        abi_path=abi_path,
    )

    ContractRegistryMap[environment][
        contract_instance.contract_address
    ] = contract_instance


def write_txn(contract_instance, function_name, args, env):
    txn = contract_instance.write(function_name, args)
    return decode_txn(txn, env)


def decode_txn(hash, environment):
    logs = get_web3().eth.getTransactionReceipt(hash).logs
    contract_wise_events = dict(
        logs | groupby(lambda x: x["address"]) | select(lambda x: (x[0], list(x[1])))
    )
    events = {}
    for contract_address in contract_wise_events:
        contract_instance = ContractRegistryMap[environment][contract_address]
        if not contract_instance:
            continue
        decoded_events = contract_instance.decode_txn(
            contract_wise_events[contract_address]
        )
        for event_name in decoded_events:
            if event_name in events.keys():
                events[event_name] += decoded_events[event_name]
            else:
                events[event_name] = decoded_events[event_name]
        events.update()
    return events
