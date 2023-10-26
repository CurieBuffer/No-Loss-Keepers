"""
Support for MakerDAO MultiCall contract
"""
import logging
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from config import MULTICALL
from eth_abi.exceptions import DecodingError
from eth_account.signers.local import LocalAccount
from eth_typing import BlockIdentifier, BlockNumber, ChecksumAddress
from hexbytes import HexBytes
from services.web3_service import Contract
from web3 import Web3
from web3._utils.abi import map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import ContractFunction
from web3.types import ABI, ABIEvent, ABIEventParams, ABIFunction, ABIFunctionParams

logger = logging.getLogger(__name__)


@dataclass
class MulticallResult:
    success: bool
    return_data: Optional[bytes]


@dataclass
class MulticallDecodedResult:
    success: bool
    return_data_decoded: Optional[Any]


def collapse_if_tuple(abi: Dict[str, Any]) -> str:
    """
    Converts a tuple from a dict to a parenthesized list of its types.

    >>> from eth_utils.abi import collapse_if_tuple
    >>> collapse_if_tuple(
    ...     {
    ...         'components': [
    ...             {'name': 'anAddress', 'type': 'address'},
    ...             {'name': 'anInt', 'type': 'uint256'},
    ...             {'name': 'someBytes', 'type': 'bytes'},
    ...         ],
    ...         'type': 'tuple',
    ...     }
    ... )
    '(address,uint256,bytes)'
    """
    typ = abi["type"]
    if not isinstance(typ, str):
        raise TypeError(
            "The 'type' must be a string, but got %r of type %s" % (typ, type(typ))
        )
    elif not typ.startswith("tuple"):
        return typ

    delimited = ",".join(collapse_if_tuple(c) for c in abi["components"])
    # Whatever comes after "tuple" is the array dims.  The ABI spec states that
    # this will have the form "", "[]", or "[k]".
    array_dim = typ[5:]
    collapsed = "({}){}".format(delimited, array_dim)

    return collapsed


def get_abi_output_types(abi: ABIFunction) -> List[str]:
    if abi["type"] == "fallback":
        return []
    else:
        return [collapse_if_tuple(cast(Dict[str, Any], arg)) for arg in abi["outputs"]]


class Multicall:
    def __init__(
        self,
        environment: str,
        default_block="latest",
    ) -> None:
        self.contract = Contract(
            contract_address=MULTICALL[environment],
            environment=environment,
            abi_path="./abis/MultiCallGnosis.json",
        )
        self.w3 = self.contract.web3
        self.default_block = default_block

    @staticmethod
    def _build_payload(
        contract_functions: Sequence[ContractFunction],
    ) -> Tuple[List[Tuple[ChecksumAddress, bytes]], List[List[Any]]]:
        targets_with_data = []
        output_types = []
        for contract_function in contract_functions:
            targets_with_data.append(
                (
                    contract_function.address,
                    HexBytes(contract_function._encode_transaction_data()),
                )
            )
            output_types.append(get_abi_output_types(contract_function.abi))
        return targets_with_data, output_types

    def _decode_data(
        self, output_type: Sequence[str], data: Optional[Any]
    ) -> Optional[Any]:
        """
        :param output_type:
        :param data:
        :return:
        :raises: DecodingError
        """
        if data:
            try:
                decoded_values = self.w3.codec.decode_abi(output_type, data)
                normalized_data = map_abi_data(
                    BASE_RETURN_NORMALIZERS, output_type, decoded_values
                )
                if len(normalized_data) == 1:
                    return normalized_data[0]
                else:
                    return normalized_data
            except DecodingError:
                logger.warning(
                    "Cannot decode %s using output-type %s", data, output_type
                )
                return data

    def _aggregate(
        self,
        targets_with_data: Sequence[Tuple[ChecksumAddress, bytes]],
    ) -> List[Optional[Any]]:
        """
        :param targets_with_data: List of target `addresses` and `data` to be called in each Contract
        :param block_identifier:
        :return:
        :raises: BatchCallFunctionFailed
        """
        aggregate_parameter = [
            {"target": target, "callData": data} for target, data in targets_with_data
        ]
        return self.contract.read(
            "aggregate", aggregate_parameter, default_block=self.default_block
        )

    def aggregate(
        self,
        contract_functions: Sequence[ContractFunction],
    ) -> List[Optional[Any]]:
        """
        Calls ``aggregate`` on MakerDAO's Multicall contract. If a function called raises an error execution is stopped
        :param contract_functions:
        :param block_identifier:
        :return: A tuple with the ``blockNumber`` and a list with the decoded return values
        :raises: BatchCallFunctionFailed
        """
        targets_with_data, output_types = self._build_payload(contract_functions)
        block_number, results = self._aggregate(targets_with_data)
        decoded_results = [
            self._decode_data(output_type, data)
            for output_type, data in zip(output_types, results)
        ]

        return decoded_results

    def write(
        self,
        contract_functions: Sequence[ContractFunction],
    ) -> List[Optional[Any]]:
        targets_with_data, output_types = self._build_payload(contract_functions)
        aggregate_parameter = [
            {"target": target, "callData": data} for target, data in targets_with_data
        ]
        txn_hash = self.contract.write("aggregate", aggregate_parameter)
        return txn_hash
