import time
from base64 import b64decode
from pacti import write_contracts_to_file
from pacti.terms.polyhedra import *
import functools
import numpy as np
from contract_utils import *
from generators import *
from typing import Callable, Optional, List, Tuple, Union

from p_tqdm import p_umap

run5 = True
run20 = True

# Now, let's apply the Latin hypercube generator to sample the scenario hyperparameters.
from scipy.stats import qmc

d = 12

o5 = 20
o20 = 20
dev_sampler = qmc.LatinHypercube(d=d)
dev_sample5: np.ndarray = dev_sampler.random(n=o5)
dev_sample20: np.ndarray = dev_sampler.random(n=o20)


nb_contracts5 = 23
nb_compose5 = 12
nb_merge5 = 10


nb_contracts20 = 115
nb_compose20 = 63
nb_merge20 = 50


m = 300
# m = 30
op_sampler: qmc.LatinHypercube = qmc.LatinHypercube(d=5)
op_sample: np.ndarray = op_sampler.random(n=m)
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
scaled_op_sample: np.ndarray = qmc.scale(sample=op_sample, l_bounds=op_l_bounds, u_bounds=op_u_bounds)


def make_merged_req(f: Callable[[np.ndarray], named_contracts_t], reqs: np.ndarray) -> merged_named_contracts_t:
    candidates: named_contracts_t = f(reqs)
    constraints: PolyhedralContract = reduce(PolyhedralContract.merge, [c for _, c in candidates])
    return (constraints, reqs, candidates)


def schedulability_analysis(
    pair: Tuple[Tuple[list[tuple2float], PolyhedralContract], merged_named_contracts_t]
) -> schedule_result_t:
    scenario: Tuple[list[tuple2float], PolyhedralContract] = pair[0]
    mreq: merged_named_contracts_t = pair[1]
    result: merge_result_t = perform_merges_seq(scenario[1], mreq)
    if isinstance(result, PolyhedralContract):
        return Schedule(scenario=scenario[0], reqs=mreq[1], contract=result)
    return result


import itertools
import pickle

from p_tqdm import p_umap


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


if run5:
    s5 = open("space_mission/data/scenarios5.data", "rb")
    scenarios = pickle.load(s5)
    s5.close()

    merged_reqs5: List[merged_named_contracts_t] = [
        make_merged_req(make_op_requirement_constraints5, req) for req in scaled_op_sample
    ]
    pairs = list(itertools.product(scenarios, merged_reqs5))
    ta = time.time()
    all_results5: list[merge_result_t] = p_umap(schedulability_analysis, pairs)
    tb = time.time()
    results5: schedule_results_t = [], []
    for r in all_results5:
        if isinstance(r, list):
            results5 = results5[0] + list[failed_merges_t](r), results5[1]
        elif isinstance(r, Schedule):
            results5 = results5[0], results5[1] + [r]
        else:
            raise ValueError("should be a merge_result_t")
    results5 = sorted(results5[0], key=lambda fm: -len(fm)), results5[1]
    print(
        f"Found {len(results5[1])} admissible and {len(results5[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios)} scenarios.\nTotal time {tb-ta} seconds."
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


if run20:
    s20 = open("space_mission/data/scenarios20.data", "rb")
    scenarios = pickle.load(s20)
    s20.close()

    merged_reqs20: List[merged_named_contracts_t] = [
        make_merged_req(make_op_requirement_constraints20, req) for req in scaled_op_sample
    ]
    pairs = list(itertools.product(scenarios, merged_reqs20))
    ta = time.time()
    all_results20: List[merge_result_t] = p_umap(schedulability_analysis, pairs)
    tb = time.time()
    results20: schedule_results_t = [], []
    for r in all_results20:
        if isinstance(r, list):
            results20 = results20[0] + list[failed_merges_t](r), results20[1]
        elif isinstance(r, Schedule):
            results20 = results20[0], results20[1] + [r]
        else:
            raise ValueError("should be a merge_result_t")
    results20 = sorted(results20[0], key=lambda fm: -len(fm)), results20[1]
    print(
        f"Found {len(results20[1])} admissible and {len(results20[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios)} scenarios.\nTotal time {tb-ta} seconds."
    )

    f = open("space_mission/data/results20.data", "wb")
    pickle.dump(results5, f)
    f.close()
