import json
import logging
import os
import time

import config
import contract
import requests
from cache import cache
from eth_account import Account
from eth_account.messages import encode_defunct
from pipe import chain, dedup, select, sort, where
from requests import Session
from retry import retry as retry_decorator
from retry_requests import TSession, retry
from timing import timing
from web3 import Web3

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
if os.getenv("DEBUG"):
    print("DEBUG")
    logging.basicConfig(level=logging.DEBUG)

keeper_account = os.environ.get("KEEPER_ACCOUNT_PK")

MAX_BATCH_SIZE = 100


@timing
@retry_decorator(tries=2)
def execute_graph_query(json_data, endpoint):
    response = retry(TSession(timeout=2), retries=2, backoff_factor=0.2).post(
        endpoint,
        json=json_data,
    )

    response.raise_for_status()

    try:
        response_json = response.json()
        if "data" not in response_json:
            print(json_data)
            print(endpoint)
            # logger.info(response_json)
            raise Exception("Error fetching from theGraph")
        return response_json  # List[{optionId, contractAddress, expirationTime}]
    except KeyError as e:
        logger.exception(f"Error fetching from theGraph {e}")
        logger.info(response.json())
        raise e
    except json.JSONDecodeError as e:
        logger.exception(f"Error fetching from theGraph {e}")
        logger.info(response.text)
        raise e


@timing
def fetch_prices(prices_to_fetch):
    query_key = lambda x: f"{x['pair']}-{x['timestamp']}"

    cached_response = {}
    uncached_prices_to_fetch = []
    for x in prices_to_fetch:
        val = cache.get(query_key(x))
        if val:
            cached_response[query_key(x)] = json.loads(val)
        else:
            uncached_prices_to_fetch.append(x)

    reqUrl = (
        os.environ.get("ORACLE_BASE_API", "https://oracle.buffer.finance")
        + "/price/query/"
    )
    fetched_prices = []
    if uncached_prices_to_fetch:

        @timing
        def f(uncached_prices_to_fetch):
            try:
                r = retry(TSession(timeout=5), retries=10, backoff_factor=0.1).post(
                    reqUrl, json=uncached_prices_to_fetch
                )
                try:
                    r.raise_for_status()
                except Exception as e:
                    logger.exception(r.text)
                    raise e

                fetched_prices = r.json()

                return dict(
                    fetched_prices
                    | where(lambda x: x["signature"] is not None)
                    | select(
                        lambda x: (
                            query_key(x),
                            {"price": x["price"], "signature": x["signature"]},
                        )
                    )
                )
            except Exception as e:
                logger.exception(f"Error fetching prices {e}")
                return None

        response = f(uncached_prices_to_fetch)
        NUM_RETRY = 10
        while not response and NUM_RETRY > 0:
            # time.sleep(0.1)
            response = f(uncached_prices_to_fetch)
            NUM_RETRY -= 1

        if response:
            now = time.time()
            try:
                logger.info(
                    f"#### Price Fetching Lags: {list(list(response.keys()) | select(lambda x: (x, round(now - int(x.split('-')[1]), 2))))}"
                )
            except Exception as e:
                logger.exception(e)

            # Cache the response so that we don't have to fetch it again
            for k, v in response.items():
                cache.set(k, json.dumps(v), ex=7200)

        response.update(cached_response)
        return response
        # asset_pair-timestamp ==> price

    return cached_response


def get_asset_pair(option_contract_address, environment):
    r = cache.get(f"{option_contract_address}-{environment}-asset_pair")
    if r:
        return r
    r = contract.get(
        option_contract_address, environment, "./abis/BufferOptions.json"
    ).read("assetPair")
    cache.set(f"{option_contract_address}-{environment}-asset_pair", r)
    return r


@timing
def get_option_to_execute(environment):
    limit = 500
    min_timestamp = int(time.time())

    json_data = {
        "query": f"""
        query UserOptionHistory($currentTimestamp: BigInt = {int(time.time())}, $minTimestamp: BigInt = {min_timestamp}) {{
            userOptionDatas(
                orderBy: creationTime
                orderDirection: asc
                where: {{state_in: [1], expirationTime_lt: $currentTimestamp, queueID_not: null}}
                first: {limit}
            ) {{
                optionID
                queueID
                optionContract {{
                    address
                }}
                expirationTime
            }}
        }}""",
        "variables": None,
        "operationName": "UserOptionHistory",
        "extensions": {
            "headers": None,
        },
    }
    # Fetch from theGraph
    expired_options = []
    try:
        expired_options = execute_graph_query(
            json_data, config.GRAPH_ENDPOINT[environment]
        )["data"][
            "userOptionDatas"
        ]  # List[{optionID, contractAddress, expirationTime}]
    except Exception as e:
        logger.exception(f"Error fetching from theGraph")
        time.sleep(5)

    expired_options = list(
        list(expired_options)
        | select(
            lambda x: {
                **x,
                "contractAddress": Web3.toChecksumAddress(
                    x["optionContract"]["address"]
                ),
                "optionID": int(x["optionID"]),
                "expirationTime": int(x["expirationTime"]),
            }
        )
    )

    # logger.info(f"expired_options: {expired_options}")
    return expired_options


@timing
def get_option_to_open(environment):
    limit = 1000
    json_data = {
        "query": f"""
        query MyQuery($currentTimestamp: BigInt = {int(time.time())}) {{
            queuedOptionDatas(
                orderBy: queueID
                orderDirection: asc
                where: {{state_in: [4], queueID_not: null}}
                first: {limit}
            ) {{
                queueID
                state
            }}
        }}""",
        "variables": None,
        "operationName": "MyQuery",
        "extensions": {
            "headers": None,
        },
    }

    queuedOptionDatas = []
    try:
        response = execute_graph_query(
            json_data,
            config.GRAPH_ENDPOINT[environment],
        )
        queuedOptionDatas = response["data"]["queuedOptionDatas"]
    except Exception as e:
        # logger.info(f"Error fetching from theGraph")
        pass
    return queuedOptionDatas


if __name__ == "__main__":
    import time

    now = int(time.time()) - 2

    start = time.time()
    print(
        fetch_prices(
            prices_to_fetch=[
                {
                    "pair": "BTCUSD",
                    "timestamp": int(time.time()),
                }
            ]
        )
    )
    end = time.time()
    print(f"Time taken: {end - start}")

    start = time.time()
    print(
        fetch_prices(
            prices_to_fetch=[
                {
                    "pair": "BTCUSD",
                    "timestamp": int(time.time()) - 1,
                }
            ]
        )
    )
    end = time.time()
    print(f"Time taken: {end - start}")

    start = time.time()
    print(
        fetch_prices(
            prices_to_fetch=[
                {
                    "pair": "ETHUSD",
                    "timestamp": int(time.time()) - 20,
                }
            ]
        )
    )
    end = time.time()
    print(f"Time taken: {end - start}")
#
