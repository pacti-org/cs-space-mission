import time
from pacti.terms.polyhedra import *
import functools
import numpy as np
from contract_utils import *
from generators import *
from typing import List, Tuple

import pickle
from pathos.helpers import cpu_count
from p_tqdm import p_umap

# Now, let's apply the Latin hypercube generator to sample the scenario hyperparameters.
from scipy.stats import qmc

run5 = True
run20 = True


op_l_bounds = [
    90.0,  # power: low range of initial soc
    5.0,  # power: low range of exit soc at each step
    5.0,  # alloc: low range of delta t
    60.0,  # sci: low range of d
    40.0,  # nav: low range of u
]
op_u_bounds = [
    100.0,  # power: high range of initial soc
    30.0,  # power: low range of exit soc at each step
    100.0,  # alloc: high range of delta t
    100.0,  # sci: high range of  d
    90.0,  # nav: high range of  u
]


op_sampler: qmc.LatinHypercube = qmc.LatinHypercube(d=len(op_l_bounds))

m = 300
# m = 20

op_sample: np.ndarray = op_sampler.random(n=m)

scaled_op_sample: np.ndarray = qmc.scale(sample=op_sample, l_bounds=op_l_bounds, u_bounds=op_u_bounds)


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
    scenario: Tuple[list[tuple2float], PolyhedralContract], reqs: np.ndarray
) -> schedule_result_t:
    """
    Schedulability analysis for the 5-step scenario sequence.

    Args:
        scenario: A tuple of hyperparameters and a scenario contract
        reqs: operational requirements

    Returns:
        A tuple...
    """
    op_reqs: named_contracts_t = make_op_requirement_constraints5(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralContract):
        return Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return result


if run5:
    s5 = open("space_mission/data/scenarios5.data", "rb")
    scenarios5 = pickle.load(s5)
    s5.close()

    srs = [(scenario, req) for scenario in scenarios5 for req in scaled_op_sample]
    ta = time.time()
    all_results5: List[schedule_result_t] = p_umap(lambda sr: schedulability_analysis5(sr[0], sr[1]), srs, num_cpus=32)
    tb = time.time()
    results5: schedule_results_t = aggregate_schedule_results(all_results5)
    print(
        f"Found {len(results5[1])} admissible and {len(results5[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios5)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios5)} scenarios.\n"
        f"Total time {tb-ta} seconds with up to {cpu_count()} CPUs."
    )

    f = open("space_mission/data/results5.data", "wb")
    pickle.dump(results5, f)
    f.close()


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
    scenario: Tuple[List[tuple2float], PolyhedralContract], reqs: np.ndarray
) -> schedule_result_t:
    op_reqs: named_contracts_t = make_op_requirement_constraints20(reqs)
    result: merge_result_t = perform_merges_seq(scenario[1], op_reqs)
    if isinstance(result, PolyhedralContract):
        return Schedule(scenario=scenario[0], reqs=reqs, contract=result)
    return result


if run20:
    s20 = open("space_mission/data/scenarios20.data", "rb")
    scenarios20 = pickle.load(s20)
    s20.close()

    srs = [(scenario, req) for scenario in scenarios20 for req in scaled_op_sample]

    ta = time.time()
    all_results20: List[schedule_result_t] = p_umap(lambda sr: schedulability_analysis20(sr[0], sr[1]), srs)
    tb = time.time()
    results20: schedule_results_t = aggregate_schedule_results(all_results20)
    print(
        f"Found {len(results20[1])} admissible and {len(results20[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios20)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios20)} scenarios.\n"
        f"Total time {tb-ta} seconds with up to {cpu_count()} CPUs."
    )

    f = open("space_mission/data/results20.data", "wb")
    pickle.dump(results20, f)
    f.close()
