import time
from pacti.terms.polyhedra import *
import os
import numpy as np
from contract_utils import *
from generators import *

from typing import Tuple

from p_tqdm import p_umap

# Now, let's apply the Latin hypercube generator to sample the scenario hyperparameters.
from scipy.stats import qmc

import pickle
from pathos.helpers import cpu_count

run5 = True
run20 = True

# Hyperparameter ranges
l_bounds = [
    2.0,  # power: min dns cons
    2.5,  # power: min chrg gen
    0.3,  # power: min sbo cons
    0.2,  # power: min tcm_h cons
    0.1,  # power: min tcm_dv cons
    5.0,  # science: min dsn speed
    2.0,  # science: min sbo gen
    1.0,  # nav: min dsn noise
    1.0,  # nav: min chrg noise
    0.5,  # nav: min sbo imp
    1.2,  # nav: min tcm_dv noise
    0.3,  # nav: min tcm_dv progress
]
u_bounds = [
    2.2,  # power: max dns cons
    3.5,  # power: max chrg gen
    0.4,  # power: max sbo cons
    0.3,  # power: max tcm_h cons
    0.2,  # power: max tcm_dv cons
    6.0,  # science: max dsn speed
    8.0,  # science: max sbo gen
    1.2,  # nav: max dsn noise
    1.2,  # nav: max chrg noise
    0.8,  # nav: max sbo imp
    1.4,  # nav: max tcm_dv noise
    0.5,  # nav: max tcm_dv progress
]

mean_sampler = qmc.LatinHypercube(d=len(l_bounds))
dev_sampler = qmc.LatinHypercube(d=len(l_bounds))

if run5:
    n5 = 200
    mean_sample5: np.ndarray = mean_sampler.random(n=n5)
    scaled_mean_sample5: np.ndarray = qmc.scale(sample=mean_sample5, l_bounds=l_bounds, u_bounds=u_bounds)
    dev_sample5: np.ndarray = dev_sampler.random(n=n5)

    nb_5step_operations = OperationCounts(contracts=23, compositions=12, merges=10)

    ta = time.time()
    scenarios5: List[Tuple[List[tuple2float], PolyhedralContract]] = p_map(generate_5step_scenario, list(zip(scaled_mean_sample5, dev_sample5)))
    tb = time.time()

    print(
        f"Generated {n5} hyperparameter variations of the 5-step scenario in {tb-ta} seconds.\n"
        f"Running on {cpu_info_message}\n"
        f"Total count of Pacti operations for each 5-step scenario: {nb_5step_operations}."
    )
    s = open("space_mission/data/scenarios5.data", "wb")
    pickle.dump(scenarios5, s)
    s.close()

if run20:
    n20 = 200
    # n20 = 100
    # n20 = 50
    mean_sample20: np.ndarray = mean_sampler.random(n=n20)
    scaled_mean_sample20: np.ndarray = qmc.scale(sample=mean_sample20, l_bounds=l_bounds, u_bounds=u_bounds)
    dev_sample20: np.ndarray = dev_sampler.random(n=n20)

    nb_20step_operations = OperationCounts(contracts=115, compositions=63, merges=50)

    ta = time.time()
    scenarios20: List[Tuple[List[tuple2float], PolyhedralContract]] = p_umap(generate_20step_scenario, list(zip(scaled_mean_sample20, dev_sample20)))
    tb = time.time()

    print(
        f"Generated {n20} hyperparameter variations of the 20-step scenario in {tb-ta} seconds.\n"
        f"Running on {cpu_info_message}\n"
        f"Total count of Pacti operations for each 5-step scenario: {nb_20step_operations}."
    )
    s = open("space_mission/data/scenarios20.data", "wb")
    pickle.dump(scenarios20, s)
    s.close()
