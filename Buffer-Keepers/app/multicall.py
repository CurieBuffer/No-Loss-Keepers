from contract import get as get_contract
from pipe import select
from services.multicall_read_service import Multicall
from services.read_service import save_result_in_cache


def multicall(contract_functions, environment, default_block="latest"):
    m = Multicall(environment=environment, default_block=default_block)
    return m.aggregate(contract_functions)


def test_cached_multicall(calls, environment, index, default_block="latest"):
    result = cached_multicall(calls, environment, index, default_block)

    by_parts_results = []
    for call in calls:
        by_parts_results.append(
            get_contract(
                contract_address=call[0],
                abi_path=call[1],
                environment=environment,
                index=index,
            ).read(call[2], *call[3:], default_block=default_block)
        )
    assert by_parts_results == result, "Multicall should be equivalent to regular read"


def cached_multicall(calls, environment, default_block="latest"):
    results = multicall(
        list(
            calls
            | select(
                lambda x: get_contract(
                    contract_address=x[0],
                    abi_path=x[1],
                    environment=environment,
                ).f(x[2], *x[3:])
            )
        ),
        environment=environment,
        default_block=default_block,
    )

    # for i, result in enumerate(results):
    #     contract_address = calls[i][0]
    #     abi_path = calls[i][1]
    #     function_name = calls[i][2]
    #     args = calls[i][3:]

    #     save_result_in_cache(
    #         result,
    #         contract_address,
    #         environment,
    #         abi_path,
    #         function_name,
    #         default_block,
    #         args,
    #     )
    return results
