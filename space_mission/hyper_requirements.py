import time
from pacti.terms.polyhedra import *
import functools
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

# Now, let's apply the Latin hypercube generator to sample the requirement hyperparameters.
from scipy.stats import qmc

op_sampler: qmc.LatinHypercube = qmc.LatinHypercube(d=len(op_l_bounds))

#m = 300
m = 20

op_sample: np.ndarray = op_sampler.random(n=m)

scaled_op_sample: np.ndarray = qmc.scale(sample=op_sample, l_bounds=op_l_bounds, u_bounds=op_u_bounds)


if run5:
    s5 = open("space_mission/scenarios5.data", "rb")
    scenarios5 = pickle.load(s5)
    s5.close()

    srs = [(scenario, req) for scenario in scenarios5 for req in scaled_op_sample]
    ta = time.time()
    all_results5: List[schedule_result_t] = p_umap(schedulability_analysis5, srs)
    tb = time.time()
    results5: schedule_results_t = aggregate_schedule_results(all_results5)
    print(
        f"Found {len(results5[1])} admissible and {len(results5[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios5)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios5)} scenarios.\n"
        f"Total time {tb-ta} seconds running on {cpu_info_message}\n"
    )

    f = open("space_mission/results5.data", "wb")
    pickle.dump(results5, f)
    f.close()


if run20:
    s20 = open("space_mission/scenarios20.data", "rb")
    scenarios20 = pickle.load(s20)
    s20.close()

    srs = [(scenario, req) for scenario in scenarios20 for req in scaled_op_sample]

    ta = time.time()
    all_results20: List[schedule_result_t] = p_umap(schedulability_analysis20, srs)
    tb = time.time()
    results20: schedule_results_t = aggregate_schedule_results(all_results20)
    print(
        f"Found {len(results20[1])} admissible and {len(results20[0])} non-admissible schedules out of {len(scaled_op_sample)*len(scenarios20)} combinations generated from {len(scaled_op_sample)} variations of operational requirements for each of the {len(scenarios20)} scenarios.\n"
        f"Total time {tb-ta} seconds running on {cpu_info_message}\n"
    )

    f = open("space_mission/results20.data", "wb")
    pickle.dump(results20, f)
    f.close()
