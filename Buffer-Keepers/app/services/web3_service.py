import importlib
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

import config
import pytz
import requests
import sha3
from hexbytes import HexBytes
from pipe import dedup, groupby, select, where
from services.abi_service import get_abi
from services.read_service import read
from utility import get_web3, to_aware_datetime
from web3 import Web3
from web3._utils.events import get_event_data
from web3.gas_strategies.time_based import fast_gas_price_strategy

logger = logging.getLogger(__name__)


class Contract(object):
    def __init__(
        self,
        contract_address: str,
        abi_path: str,
        environment: str = "testnet",
    ):
        self.contract_address = self.get_checksum_address(contract_address)
        self.environment = environment
        # self.web3 = get_web3(get_read_provider(environment))
        self.abi_path = abi_path
        self.abi = get_abi(abi_path)
        self.mappings: Dict[str, str] = {}
        self.on_block_mappings: List[str] = []
        self.events_to_scan = None

    @property
    def web3(self):
        return get_web3()

    @property
    def contract_instance(self):
        return self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def get_checksum_address(self, address):
        try:
            checksum_address = Web3.toChecksumAddress(address)
        except ValueError:
            logger.exception(f"{address} is not valid")
        return checksum_address

    def decode_txn(self, data):
        data = dict(
            data
            | dedup(lambda x: (x["transactionHash"], x["logIndex"]))
            | select(lambda x: self.decode_log(event_name=None, logs=x))
            | where(lambda x: x != None)
            | groupby(lambda x: x["event_name"])
            | select(lambda x: (x[0], list(x[1] | select(lambda x: x["args"]))))
        )
        logger.debug(f"Found {len(data)} events!")
        return data

    def decode_log(self, event_name, logs):
        try:
            """
            eg. event = {
                "event_name": event_name,
                "timestamp": block_when,
                "log_index": log_index,
                "transaction_index": transaction_index,
                "txhash": txhash,
                "block_number": block_number,
                "address": event.address,
                "args": event["args"]
            }
            """
            data = dict(logs)
            data["topics"] = list(data["topics"] | where(lambda x: x != None))
            data["topics"] = list(map(HexBytes, data["topics"]))

            if not event_name:
                event_name = self.get_event_name_for_topic(data["topics"][0])

            data["transactionHash"] = HexBytes(data["transactionHash"])
            # data["transactionIndex"] = (
            #     int(data["transactionIndex"], 16) if data["transactionIndex"] != "0x" else 0
            # )
            # data["logIndex"] = int(data["logIndex"], 16) if data["logIndex"] != "0x" else 0
            data["blockHash"] = data["transactionHash"]
            # print(event_name)
            decoded_event = dict(
                get_event_data(self.web3.codec, self.get_event_abi(event_name), data)
            )

            # decoded_event["timestamp"] = to_aware_datetime(int(data["timeStamp"], 16))
            # decoded_event["block_number"] = int(data.pop("blockNumber"), 16)

            decoded_event["log_index"] = decoded_event.pop("logIndex")
            decoded_event["transaction_index"] = decoded_event.pop("transactionIndex")
            decoded_event["txhash"] = decoded_event.pop("transactionHash")
            decoded_event["event_name"] = decoded_event.pop("event")
            return decoded_event
        except Exception as e:
            # logger.exception(e)
            return None

    # @retry_on_http_error()
    def _get_nonce(self, private_key):
        return self.web3.eth.getTransactionCount(self.get_account(private_key))

    def get_gas_price(self):
        self.web3.eth.set_gas_price_strategy(fast_gas_price_strategy)
        return int(self.web3.eth.generate_gas_price())

    def write(self, function_name: str, *args, value=0):
        private_key = os.environ.get("KEEPER_ACCOUNT_PK")
        try:
            return self.publish_txn(
                getattr(self.contract_instance.functions, function_name)(*args),
                value,
                private_key,
            )
        except ValueError as e:
            if "replacement transaction underpriced" in str(e):
                logger.info(f"Txn already underway for {(function_name, args, value)}")
            if "already known" in str(e):
                # the txn is already in the mempool so we need to speed up the txn
                logger.info(
                    "the txn is already in the mempool so we need to speed up the txn"
                )
                actual_gas_price = self.get_gas_price()
                logger.info(f"Trying with gas price {actual_gas_price}")
                return self.publish_txn(
                    getattr(self.contract_instance.functions, function_name)(*args),
                    value,
                    private_key,
                    gas_price=actual_gas_price,
                )
            else:
                raise e

    def f(self, function_name, *args):
        return getattr(self.contract_instance.functions, function_name)(*args)

    def s(self, function_name, *args):
        return [self.contract_address, self.abi, function_name, *args]

    def get_account(self, private_key):
        return Web3.toChecksumAddress(
            self.web3.eth.account.privateKeyToAccount(private_key).address
        )

    def publish_txn(self, transfer_txn, value, private_key, gas_price=None):
        nonce = self._get_nonce(private_key=private_key)
        block = self.web3.eth.get_block("latest")
        base_fee = block["baseFeePerGas"]

        default_gas_price = int(config.GAS_PRICE[self.environment])
        account = self.get_account(private_key)

        transfer_txn = transfer_txn.buildTransaction(
            {
                "from": account,
                "chainId": int(os.environ.get("CHAIN_ID")),
                # "gas": 10_000_000,
                # "gasPrice": gas_price if gas_price else default_gas_price,
                # "gasPrice": self.get_gas_price(),
                "nonce": nonce,
                "value": value,
                # "maxFeePerGas": base_fee * 2,
                # "maxPriorityFeePerGas": gas_price if gas_price else default_gas_price,
            }
        )
        gas = self.web3.eth.estimate_gas(transfer_txn) * 1.5
        transfer_txn.update({"gas": int(gas * 2)})

        signed_txn = self.web3.eth.account.sign_transaction(
            transfer_txn, private_key=private_key
        )

        try:
            self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        except ValueError as e:
            error_message = str(e)
            if "nonce too low" in error_message:
                # TODO: if this gets stuck for too long then do something about it
                logger.warning(
                    f"nonce too low: {self.environment}-{account}. Skipping for now"
                )
            elif (
                "replacement transaction underpriced" in error_message
                or "already known" in error_message
            ):
                # TODO: if this gets stuck for too long then do something about it
                logger.warning(
                    f"Txn {self.environment}:{ Web3.toHex(signed_txn.hash)} still in progress"
                )

            else:
                logger.exception(f"Write call failing for {self.environment}")
        except requests.HTTPError as e:
            if "Too Many Requests" in str(e):
                # if its a testnet chain just ignore such errors
                raise e
            else:
                raise e
        except:
            logger.exception(f"Write call failing for {self.environment}")

        txn_hash = self.web3.toHex(Web3.keccak(signed_txn.rawTransaction))
        self.web3.eth.wait_for_transaction_receipt(txn_hash)
        # receipt = self.web3.eth.getTransactionReceipt(txn_hash)
        logger.info(
            f"View txn at https://{os.environ.get('EXPLORER', 'goerli.arbiscan.io')}/tx/{txn_hash}"
        )

        new_nonce = self._get_nonce(private_key=private_key)
        start_time = int(time.time())
        while new_nonce == nonce:
            if (int(time.time()) - start_time) > 60 * 2:
                logger.info("Confirmation taking too long, leaving this for now...")
                break
            time.sleep(2)
            new_nonce = self._get_nonce(private_key=private_key)

        return txn_hash

    def read(
        self, function_name: str, *args, default_block="latest", caller_address=None
    ):
        return read(
            self.contract_address,
            self.environment,
            self.abi,
            function_name,
            default_block,
            caller_address,
            args,
        )

    def get_event_name_for_topic(self, topic0):
        if not hasattr(self, "topic_to_event_name_mapping"):
            self.topic_to_event_name_mapping = dict(
                list(
                    self.get_all_event_names()
                    | select(
                        lambda event_name: (self.get_topic(event_name), event_name)
                    )
                )
            )
        try:
            if isinstance(topic0, HexBytes):
                topic0 = topic0.hex()
            return self.topic_to_event_name_mapping[topic0]
        except:
            event_abi = self.get_abi_for_topic(topic0)
            return event_abi.get("name")

    def get_abi_for_topic(self, topic0):
        if isinstance(topic0, HexBytes):
            topic0 = topic0.hex()
        if hasattr(self, "topic_to_abi_mapping"):
            return self.topic_to_abi_mapping[topic0]

        self.topic_to_abi_mapping = dict(
            list(
                self.get_all_event_names()
                | select(
                    lambda event_name: (
                        self.get_topic(event_name),
                        self.get_event_abi(event_name),
                    )
                )
            )
        )
        return self.topic_to_abi_mapping.get(topic0, {})

    def get_all_event_types(self):
        return list(
            self.get_all_event_names()
            | select(
                lambda event_name: getattr(self.contract_instance.events, event_name)
            )
        )

    def get_all_event_names(self):
        return list(
            self.contract_instance.abi
            | where(lambda x: x["type"] == "event")
            | select(lambda x: x["name"])
        )

    def get_event_abi(self, event_name):
        var_name = "__var_event_abi"
        if hasattr(self, var_name):
            if event_name in getattr(self, var_name):
                return getattr(self, var_name)[event_name]
        else:
            setattr(self, var_name, {})

        data = list(
            filter(lambda x: x.get("name") == event_name, self.contract_instance.abi)
        )
        if data:
            data = data[0]
        else:
            logger.exception("Invalid Event Name")

        getattr(self, var_name)[event_name] = data
        return data

    def get_topic(self, event_name):
        var_name = "__var_get_topic"
        if hasattr(self, var_name):
            if event_name in getattr(self, var_name):
                return getattr(self, var_name)[event_name]
        else:
            setattr(self, var_name, {})

        data = self.get_event_abi(event_name)
        input_types = list(data["inputs"] | select(lambda x: x["type"]))
        input_type_string = ",".join(input_types)
        message = f"{data['name']}({input_type_string})"

        k = sha3.keccak_256()
        k.update(message.encode("utf-8"))

        _topic = f"0x{k.hexdigest()}"

        getattr(self, var_name)[event_name] = _topic
        return _topic

    def __str__(self):
        return f"{self.contract_address} on {self.environment} with {self.abi_path}"

    def __repr__(self):
        return f"{self.contract_address} on {self.environment} with {self.abi_path}"

    def json(self):
        fields = [
            "contract_address",
            "environment",
            "abi_path",
            "mappings",
            "on_block_mappings",
            "index",
            "event_scan",
        ]
        return {field: self.__dict__[field] for field in fields}


def get_contract_instance(**kwargs):
    contract_instance = Contract(
        contract_address=kwargs["contract_address"],
        environment=kwargs["environment"],
        abi_path=kwargs["abi_path"],
    )

    return contract_instance
