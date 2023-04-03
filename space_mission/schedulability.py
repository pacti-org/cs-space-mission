from pacti.terms.polyhedra import *
import functools
import numpy as np
from contract_utils import *
from generators import *
from typing import List, Tuple


def make_op_requirement_constraints5(reqs: np.ndarray) -> named_contracts_t:
    cs1: named_contracts_t = [
        (
            "durations",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[var], output_vars=[], assumptions=[f"-{var} <= -{reqs[2]}"], guarantees=[]
                    )
                    for var in [
                        "duration_dsn1",
                        "duration_charging2",
                        "duration_sbo3",
                        "duration_tcm_h4",
                        "duration_tcm_dv5",
                    ]
                ],
            ),
        )
    ]
    cs2: named_contracts_t = [
        (
            "initial",
            PolyhedralContract.from_string(
                input_vars=["soc1_entry", "c1_entry", "d1_entry", "u1_entry", "r1_entry"],
                output_vars=[],
                assumptions=[
                    f"-soc1_entry <= -{reqs[0]}",
                    f"c1_entry = 0",
                    f"d1_entry={reqs[3]}",
                    f"u1_entry={reqs[4]}",
                    f"r1_entry = 100",
                ],
                guarantees=[],
            ),
        )
    ]
    cs3: named_contracts_t = [
        (
            "output_soc",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"-output_soc{i} <= -{reqs[1]}"],
                    )
                    for i in range(1, 6)
                ],
            ),
        )
    ]
    return cs1 + cs2 + cs3


def schedulability_analysis5(
    scenario_reqs: Tuple[Tuple[list[tuple2float], PolyhedralContract], np.ndarray]
) -> schedule_result_t:
    scenario = scenario_reqs[0]
    reqs = scenario_reqs[1]
    op_reqs: named_contracts_t = make_op_requirement_constraints5(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralContract):
        return Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return result


def make_op_requirement_constraints20(reqs: np.ndarray) -> named_contracts_t:
    cs1: named_contracts_t = [
        (
            "durations",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[var], output_vars=[], assumptions=[f"-{var} <= -{reqs[2]}"], guarantees=[]
                    )
                    for var in [
                        "duration_dsn1",
                        "duration_charging2",
                        "duration_sbo3",
                        "duration_tcm_h4",
                        "duration_tcm_dv5",
                        "duration_dsn6",
                        "duration_charging7",
                        "duration_sbo8",
                        "duration_tcm_h9",
                        "duration_tcm_dv10",
                        "duration_dsn11",
                        "duration_charging12",
                        "duration_sbo13",
                        "duration_tcm_h14",
                        "duration_tcm_dv15",
                        "duration_dsn16",
                        "duration_charging17",
                        "duration_sbo18",
                        "duration_tcm_h19",
                        "duration_tcm_dv20",
                    ]
                ],
            ),
        )
    ]
    cs2: named_contracts_t = [
        (
            "initial",
            PolyhedralContract.from_string(
                input_vars=["soc1_entry", "c1_entry", "d1_entry", "u1_entry", "r1_entry"],
                output_vars=[],
                assumptions=[
                    f"-soc1_entry <= -{reqs[0]}",
                    f"c1_entry = 0",
                    f"d1_entry={reqs[3]}",
                    f"u1_entry={reqs[4]}",
                    f"r1_entry = 100",
                ],
                guarantees=[],
            ),
        )
    ]
    cs3: named_contracts_t = [
        (
            "output_soc1-5",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"-output_soc{i} <= -{reqs[1]}"],
                    )
                    for i in range(1, 6)
                ],
            ),
        )
    ]
    cs4: named_contracts_t = [
        (
            "output_soc6-10",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"-output_soc{i} <= -{reqs[1]}"],
                    )
                    for i in range(5, 11)
                ],
            ),
        )
    ]
    cs5: named_contracts_t = [
        (
            "output_soc11-15",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"-output_soc{i} <= -{reqs[1]}"],
                    )
                    for i in range(10, 16)
                ],
            ),
        )
    ]
    cs6: named_contracts_t = [
        (
            "output_soc16-20",
            functools.reduce(
                PolyhedralContract.merge,
                [
                    PolyhedralContract.from_string(
                        input_vars=[],
                        output_vars=[f"output_soc{i}"],
                        assumptions=[],
                        guarantees=[f"-output_soc{i} <= -{reqs[1]}"],
                    )
                    for i in range(15, 21)
                ],
            ),
        )
    ]
    return cs1 + cs2 + cs3 + cs4 + cs5 + cs6


def schedulability_analysis20(
    scenario_reqs: Tuple[Tuple[list[tuple2float], PolyhedralContract], np.ndarray]
) -> schedule_result_t:
    scenario = scenario_reqs[0]
    reqs = scenario_reqs[1]
    op_reqs: named_contracts_t = make_op_requirement_constraints20(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralContract):
        return Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return result
