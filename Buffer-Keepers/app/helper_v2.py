import json
import logging
import os
import time

import config
import contract
import requests
from cache import cache
from config import ROUTER, ZERO_ADDRESS
from data_v2 import (
    fetch_prices,
    get_asset_pair,
    get_option_to_execute,
    get_option_to_open,
)
from eth_account import Account
from eth_account.messages import encode_defunct
from multicall import cached_multicall
from pipe import chain, dedup, select, sort, where
from timing import timing
from utility import get_account

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


keeper_account = os.environ["KEEPER_ACCOUNT_PK"]
MAX_BATCH_SIZE = 100

from pipe import Pipe


def _(x):
    return json.dumps(x, indent=4, sort_keys=True)


def get_target_contract_mapping(d, environment):
    # Filter out the ones for invalid pairs
    target_option_contracts_mapping = list(
        d
        | select(lambda x: x["contractAddress"])
        | dedup
        | select(
            lambda options_contract: (
                options_contract,
                get_asset_pair(options_contract, environment),
            )
        )
    )

    target_option_contracts_mapping = dict(
        target_option_contracts_mapping
        | select(lambda x: (x[0], x[1].replace("-", "")))
    )
    logger.info(f"target_option_contracts_mapping: {(target_option_contracts_mapping)}")

    return target_option_contracts_mapping


def is_strike_valid(slippage, current_price, strike):
    if (current_price <= (strike * (1e4 + slippage)) / 1e4) and (
        current_price >= (strike * (1e4 - slippage)) / 1e4
    ):
        return True
    else:
        return False


@timing
def open(environment):
    router_abi = "./abis/Router.json"
    queue_ids = list(
        get_option_to_open(environment)
        | where(lambda x: x["state"] == 4)
        | select(lambda x: int(x["queueID"]))
        | dedup
        | sort(key=lambda x: x)
    )

    if queue_ids:
        logger.debug(f"Queue ids from theGraph: {_(queue_ids)}")

    unresolved_trades = []

    queue_ids = queue_ids[:MAX_BATCH_SIZE]
    unresolved_trades = list(
        list(
            zip(
                queue_ids,
                cached_multicall(
                    list(
                        queue_ids
                        | select(
                            lambda x: (
                                ROUTER[environment],
                                router_abi,
                                "queuedTrades",
                                x,
                            )
                        )
                    ),
                    environment=environment,
                ),
            )
        )
        | select(lambda x: (x[0], x[1][6], x[1][9]))
    )

    if not unresolved_trades:
        return

    logger.info(f"unresolved_trades: {_(unresolved_trades)}")

    target_option_contracts_mapping = dict(
        unresolved_trades
        | select(lambda x: x[1])
        | dedup
        | select(
            lambda options_contract: (
                options_contract,
                get_asset_pair(options_contract, environment).replace("-", ""),
            )
        )
    )

    prices_to_fetch = list(
        unresolved_trades
        | select(
            lambda x: f"{target_option_contracts_mapping[x[1]]}%{x[2]}",
        )
        | dedup
        | select(lambda x: x.split("%"))
        | select(
            lambda x: {
                "pair": x[0],
                "timestamp": int(x[1]),
            }
        )
        | sort(key=lambda x: x["timestamp"], reverse=False)
    )  # List[(assetPair, timestamp)]

    logger.debug(f"prices_to_fetch: {_(prices_to_fetch)}")
    fetched_prices_mapping = fetch_prices(prices_to_fetch)
    logger.debug(f"fetched_prices_mapping: {_(fetched_prices_mapping)}")

    _price = lambda x: fetched_prices_mapping.get(
        f"{target_option_contracts_mapping[x[1]]}-{x[2]}",
        {},
    )

    unresolved_trades = list(
        unresolved_trades
        | where(lambda x: _price(x).get("price"))
        | select(
            lambda x: (
                x[0],  # queueId
                x[2],  # timestamp
                _price(x)["price"],  # price
                _price(x)["signature"],  # signature
            )
        )
        | dedup(key=lambda x: x[0])
    )  # List[(queueId, timestamp, price, signature)]

    if unresolved_trades:
        logger.info(f"resolve payload: {_(unresolved_trades)}")
        router_contract = contract.ContractRegistryMap[environment][ROUTER[environment]]

        try:
            events = contract.write_txn(
                router_contract, "resolveQueuedTrades", unresolved_trades, environment
            )
            logger.info(f"events: {(events)}")
        except Exception as e:
            if "nonce too low" in str(e):
                logger.info(e)
            else:
                logger.exception(e)


def unlock_options(environment):
    options_abi = "./abis/BufferOptions.json"
    expired_options = get_option_to_execute(environment)
    if not expired_options:
        return

    logger.debug(f"expired_options from theGraph: {_(expired_options)}")

    # Filter out the ones for invalid pairs
    target_option_contracts_mapping = list(
        expired_options
        | select(lambda x: x["contractAddress"])
        | dedup
        | select(
            lambda options_contract: (
                options_contract,
                get_asset_pair(options_contract, environment),
            )
        )
    )

    target_option_contracts_mapping = dict(
        target_option_contracts_mapping
        | select(lambda x: (x[0], x[1].replace("-", "")))
    )

    # Take the initial 100
    expired_options = expired_options[:MAX_BATCH_SIZE]

    expired_options = list(
        list(
            zip(
                expired_options,
                cached_multicall(
                    list(
                        expired_options
                        | select(
                            lambda x: (
                                x["contractAddress"],
                                options_abi,
                                "options",
                                x["optionID"],
                            )
                        )
                    ),
                    environment=environment,
                ),
            )
        )
        | where(lambda x: x[1][0] == 1)
        | select(lambda x: x[0])
    )

    if not expired_options:
        return

    logger.info(f"expired_options: {_(expired_options)}")
    # Fetch the prices for the valid ones
    prices_to_fetch = list(
        expired_options
        | select(
            lambda x: f'{target_option_contracts_mapping[x["contractAddress"]]}%{x["expirationTime"]}',
        )
        | dedup
        | select(lambda x: x.split("%"))
        | select(
            lambda x: {
                "pair": x[0],
                "timestamp": int(x[1]),
            }
        )
    )  # List[(assetPair, timestamp)]

    logger.debug(f"prices_to_fetch: {_(prices_to_fetch)}")
    fetched_prices_mapping = fetch_prices(prices_to_fetch)

    _price = lambda x: fetched_prices_mapping.get(
        f"{target_option_contracts_mapping[x['contractAddress']]}-{x['expirationTime']}",
        {},
    )

    unlock_payload = list(
        expired_options
        | where(lambda x: _price(x).get("price"))
        | select(
            lambda x: (
                x["optionID"],
                x["contractAddress"],
                x["expirationTime"],
                _price(x)["price"],  # price
                _price(x)["signature"],  # signature
            )
        )
        | dedup(key=lambda x: f"{x[0]}-{x[1]}")
    )

    if unlock_payload:
        logger.info(f"unlock_payload: {_(unlock_payload)}")
        router_contract = contract.ContractRegistryMap[environment][ROUTER[environment]]

        try:
            events = contract.write_txn(
                router_contract, "unlockOptions", unlock_payload, environment
            )
            logger.info(f"events: {(events)}")
        except Exception as e:
            if "nonce too low" in str(e):
                logger.info(e)
            else:
                logger.exception(e)


def register_all_contracts(environment):
    contract.register(ROUTER[environment], environment, "./abis/Router.json")
    logger.info("All contracts registered")


if __name__ == "__main__":
    register_all_contracts("arb-sandbox")
    open("arb-sandbox")
