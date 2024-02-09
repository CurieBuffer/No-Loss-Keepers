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
    get_vaa_for_a_specific_time,
)
from eth_account import Account
from eth_account.messages import encode_defunct
from multicall import cached_multicall
from pipe import chain, dedup, select, sort, where
from pyth import FEED_ID_PYTH_SYMBOL_MAPPING
from timing import timing
from utility import get_account

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


keeper_account = os.environ["KEEPER_ACCOUNT_PK"]
MAX_BATCH_SIZE = 100
pyth_abi = "./abis/Pyth.json"

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


def get_price_data(asset_time_mapping, environment):
    price_update_data = dict(
        asset_time_mapping
        | select(
            lambda x: (
                f"{x[0]}-{x[1]}",
                get_vaa_for_a_specific_time(x[0], int(x[1]), environment),
            )
        )
    )  # List[(assetPair, timestamp)]
    pyth_contract = contract.ContractRegistryMap[environment][config.PYTH[environment]]

    total_fee = sum(
        list(
            asset_time_mapping
            | select(
                lambda x: pyth_contract.read(
                    "getUpdateFee", price_update_data[f"{x[0]}-{x[1]}"]
                )
            )
        )
        # list(
        #     cached_multicall(
        #         list(
        #             asset_time_mapping
        #             | select(
        #                 lambda x: (
        #                     config.PYTH[environment],
        #                     pyth_abi,
        #                     "getUpdateFee",
        #                     price_update_data[f"{x[0]}-{x[1]}"],
        #                 )
        #             )
        #         ),
        #         environment=environment,
        #     )
        # )
    )
    return price_update_data, total_fee


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
    router_contract = contract.ContractRegistryMap[environment][ROUTER[environment]]

    queue_ids = queue_ids[:MAX_BATCH_SIZE]
    unresolved_trades = list(
        list(
            zip(
                queue_ids,
                list(
                    queue_ids
                    | select(lambda x: router_contract.read("queuedTrades", x))
                ),
                # cached_multicall(
                #     list(
                #         queue_ids
                #         | select(
                #             lambda x: (
                #                 ROUTER[environment],
                #                 router_abi,
                #                 "queuedTrades",
                #                 x,
                #             )
                #         )
                #     ),
                #     environment=environment,
                # ),
            )
        )
        | where(lambda x: x[1][10])
        | select(
            lambda x: {
                "queueId": x[0],
                "contractAddress": x[1][6],
                "isAbove": x[1][5],
                "queueTimestamp": x[1][9],
            }
        )
    )

    if not unresolved_trades:
        return

    logger.info(f"unresolved_trades: {_(unresolved_trades)}")

    target_option_contracts_mapping = get_target_contract_mapping(
        unresolved_trades, environment
    )

    _asset = lambda x: target_option_contracts_mapping[x["contractAddress"]]
    asset_time_mapping = list(
        unresolved_trades
        | select(
            lambda x: f"{target_option_contracts_mapping[x['contractAddress']]}%{x['queueTimestamp']}",
        )
        | select(lambda x: x.split("%"))
    )
    logger.info(f"asset_time_mapping: {(asset_time_mapping)}")

    price_update_data, total_fee = get_price_data(asset_time_mapping, environment)

    unresolved_trades = list(
        unresolved_trades
        | select(
            lambda x: (
                int(x["queueId"]),  # queueId
                price_update_data[f"{_asset(x)}-{x['queueTimestamp']}"],
                [FEED_ID_PYTH_SYMBOL_MAPPING[_asset(x)]],
            )
        )
        | dedup(key=lambda x: x[0])
    )  # List[(queueId, timestamp, price, signature)]

    if unresolved_trades:
        logger.info(f"resolve payload: {(unresolved_trades)}")

        try:
            events = contract.write_txn(
                router_contract,
                "resolveQueuedTrades",
                environment,
                unresolved_trades,
                value=total_fee,
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
                list(
                    expired_options
                    | select(
                        lambda x: contract.get_contract_instance(
                            contract_address=contract.get_checksum_address(
                                x["contractAddress"]
                            ),
                            environment=environment,
                            abi_path="./abis/BufferOptions.json",
                        ).read("options", x["optionID"])
                    )
                ),
                # cached_multicall(
                #     list(
                #         expired_options
                #         | select(
                #             lambda x: (
                #                 x["contractAddress"],
                #                 options_abi,
                #                 "options",
                #                 x["optionID"],
                #             )
                #         )
                #     ),
                #     environment=environment,
                # ),
            )
        )
        | where(lambda x: x[1][0] == 1)
        | select(lambda x: x[0])
    )

    if not expired_options:
        return

    logger.info(f"expired_options: {_(expired_options)}")

    target_option_contracts_mapping = get_target_contract_mapping(
        expired_options, environment
    )
    asset_time_mapping = list(
        expired_options
        | select(
            lambda x: f"{target_option_contracts_mapping[x['contractAddress']]}%{x['expirationTime']}",
        )
        | select(lambda x: x.split("%"))
    )

    price_update_data, total_fee = get_price_data(asset_time_mapping, environment)
    _asset = lambda x: target_option_contracts_mapping[x["contractAddress"]]

    unlock_payload = list(
        expired_options
        | select(
            lambda x: (
                x["optionID"],
                x["contractAddress"],
                price_update_data[f'{_asset(x)}-{x["expirationTime"]}'],
                [FEED_ID_PYTH_SYMBOL_MAPPING[_asset(x)]],
            )
        )
        | dedup(key=lambda x: f"{x[0]}-{x[1]}")
    )

    if unlock_payload:
        logger.info(f"unlock_payload: {(unlock_payload)}")
        router_contract = contract.ContractRegistryMap[environment][ROUTER[environment]]

        try:
            events = contract.write_txn(
                router_contract,
                "unlockOptions",
                environment,
                unlock_payload,
                value=total_fee,
            )
            logger.info(f"events: {(events)}")
        except Exception as e:
            if "nonce too low" in str(e):
                logger.info(e)
            else:
                logger.exception(e)


def register_all_contracts(environment):
    contract.register(ROUTER[environment], environment, "./abis/Router.json")
    contract.register(config.PYTH[environment], environment, "./abis/Pyth.json")
    logger.info("All contracts registered")


if __name__ == "__main__":
    register_all_contracts("arb-sandbox")
    open("arb-sandbox")
