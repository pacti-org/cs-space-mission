import time
from pacti.terms.polyhedra import PolyhedralTermList
from pacti.contracts import PolyhedralIoContract
from pacti_instrumentation.pacti_counters import summarize_instrumentation_data
import numpy as np
from contract_utils import *
from generators import *
from typing import List, Tuple
from schedulability import *

import pickle
from p_tqdm import p_umap

run5 = True
run20 = True


op_l_bounds = [
    90.0,  # power: low range of initial soc
    5.0,   # power: low range of exit soc at each step
    5.0,   # alloc: low range of delta t
    60.0,  # sci: low range of d
    40.0,  # nav: low range of u
    60.0,  # nav: low range of r
]
op_u_bounds = [
    100.0,  # power: high range of initial soc
    30.0,   # power: low range of exit soc at each step
    100.0,  # alloc: high range of delta t
    100.0,  # sci: high range of  d
    90.0,   # nav: high range of  u
    100.0,  # nav: high range of r
]

# Now, let's apply the Latin hypercube generator to sample the requirement hyperparameters.
from scipy.stats import qmc

op_sampler: qmc.LatinHypercube = qmc.LatinHypercube(d=len(op_l_bounds))

m = 100
#m = 20

K = 5  # Replace 5 with the desired group size

op_sample: np.ndarray = op_sampler.random(n=m)

scaled_op_sample: np.ndarray = qmc.scale(sample=op_sample, l_bounds=op_l_bounds, u_bounds=op_u_bounds)


if run5:
    s5 = open("space_mission/scenarios5.data", "rb")
    scenarios5: list[tuple[List[tuple2float], PolyhedralIoContract]] = pickle.load(s5)
    s5.close()

    for i, scenario in enumerate(scenarios5):
        c: PolyhedralIoContract = scenario[1]
        g: PolyhedralTermList = c.g
        for t in g.terms:
            if len(t.vars) == 1 and t.vars[0] in c.inputvars:
                print(f"scenario[{i}] has a guarantee involving a single input variable: {t}")



    srs = [(scenario, req) for scenario in scenarios5 for req in scaled_op_sample]

    if K > 1:
        grouped_srs = [tuple(srs[i:i + K]) for i in range(0, len(srs), K)]
        ta = time.time()
        results_5g: List[List[Tuple[PactiInstrumentationData, schedule_result_t]]] = p_umap(schedulability_analysis5_grouped, grouped_srs)
        tb = time.time()
        flat_results = [result for group in results_5g for result in group]
        stats = summarize_instrumentation_data([result[0] for result in flat_results])
        all_results5 = [result[1] for result in flat_results if result[1]]
    else:
        ta = time.time()
        results_5ng: List[Tuple[PactiInstrumentationData, schedule_result_t]] = p_umap(schedulability_analysis5, srs)
        tb = time.time()
        stats = summarize_instrumentation_data([result[0] for result in results_5ng])
        all_results5 = [result[1] for result in results_5ng if result[1]]

    results5: schedule_results_t = aggregate_schedule_results(all_results5)
    print(
        f"Found {len(results5[1])} admissible and {len(results5[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios5)} combinations"
        f" generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios5)} scenarios.\n"
        f"Total time {tb-ta} seconds running on {cpu_info_message}\n"
        f"{stats.stats()}"
    )

    f = open("space_mission/results5.data", "wb")
    pickle.dump(results5, f)
    f.close()


if run20:
    s20 = open("space_mission/scenarios20.data", "rb")
    scenarios20 = pickle.load(s20)
    s20.close()


    for i, scenario in enumerate(scenarios20):
        c: PolyhedralIoContract = scenario[1]
        g: PolyhedralTermList = c.g
        for t in g.terms:
            if len(t.vars) == 1 and t.vars[0] in c.inputvars:
                print(f"scenario[{i}] has a guarantee involving a single input variable: {t}")

    srs = [(scenario, req) for scenario in scenarios20 for req in scaled_op_sample]

    if K > 1:
        grouped_srs = [tuple(srs[i:i + K]) for i in range(0, len(srs), K)]
        ta = time.time()
        results_20g: List[List[Tuple[PactiInstrumentationData, schedule_result_t]]] = p_umap(schedulability_analysis5_grouped, grouped_srs)
        tb = time.time()
        flat_results = [result for group in results_20g for result in group]
        stats = summarize_instrumentation_data([result[0] for result in flat_results])
        all_results20 = [result[1] for result in flat_results if result[1]]
    else:
        ta = time.time()
        results_20ng: List[Tuple[PactiInstrumentationData, schedule_result_t]] = p_umap(schedulability_analysis20, srs)
        tb = time.time()
        stats = summarize_instrumentation_data([result[0] for result in results_20ng])
        all_results20 = [result[1] for result in results_20ng if result[1]]

    results20: schedule_results_t = aggregate_schedule_results(all_results20)
    print(
        f"Found {len(results20[1])} admissible and {len(results20[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios20)} combinations"
        f" generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios20)} scenarios.\n"
        f"Total time {tb-ta} seconds running on {cpu_info_message}\n"
        f"{stats.stats()}"
    )

    f = open("space_mission/results20.data", "wb")
    pickle.dump(results20, f)
    f.close()
