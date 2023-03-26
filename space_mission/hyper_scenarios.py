import time
import joblib
from base64 import b64decode
from pacti import write_contracts_to_file
from pacti.terms.polyhedra import *
import os
import numpy as np
from contract_utils import *
from generators import *

from typing import Optional, Tuple, Union

from tqdm.auto import tqdm
from p_tqdm import p_umap


parallelism = True
run5 = True
run20 = True

# Now, let's apply the Latin hypercube generator to sample the scenario hyperparameters.
from scipy.stats import qmc

d = 12
n5 = 200
n20 = 200
# n20 = 100
# n20 = 50

mean_sampler = qmc.LatinHypercube(d=d)
mean_sample5: np.ndarray = mean_sampler.random(n=n5)
mean_sample20: np.ndarray = mean_sampler.random(n=n20)
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
scaled_mean_sample5: np.ndarray = qmc.scale(sample=mean_sample5, l_bounds=l_bounds, u_bounds=u_bounds)
scaled_mean_sample20: np.ndarray = qmc.scale(sample=mean_sample20, l_bounds=l_bounds, u_bounds=u_bounds)

dev_sampler = qmc.LatinHypercube(d=d)
dev_sample5: np.ndarray = dev_sampler.random(n=n5)
dev_sample20: np.ndarray = dev_sampler.random(n=n20)

nb_contracts5 = 23
nb_compose5 = 12
nb_merge5 = 10

nb_contracts20 = 115
nb_compose20 = 63
nb_merge20 = 50

import itertools
import pickle

if run5:
    mean_devs = list(zip(scaled_mean_sample5, dev_sample5))
    print(f"Generating {len(mean_devs)} hyperparameter variations of the 5-step scenario")
    ta = time.time()
    scenarios5: List[Tuple[List[tuple2float], PolyhedralContract]] = p_umap(lambda md: make_scenario(1, md[0], md[1], True), mean_devs)
    tb = time.time()

    if scenarios5:
        print(f"All {len(scenarios5)} hyperparameter variations of the 5-step scenario sequence generated in {tb-ta} seconds.")
        print(
            f"Total count of Pacti operations: {nb_contracts5} contracts; {nb_merge5} merges; and {nb_compose5} compositions."
        )
        s = open("space_mission/data/scenarios5.data", "wb")
        pickle.dump(scenarios5, s)
        s.close()

if run20:
    mean_devs = list(zip(scaled_mean_sample20, dev_sample20))
    print(f"Generating {len(mean_devs)} hyperparameter variations of the 5-step scenario")
    ta = time.time()
    scenarios20: List[Tuple[List[tuple2float], PolyhedralContract]] = p_umap(lambda md: long_scenario(md[0], md[1]), mean_devs)
    tb = time.time()

    if scenarios20:
        print(
            f"All {len(scenarios20)} hyperparameter variations of the 20-step scenario sequence generated.\nTotal time {tb-ta} seconds using a maximum of {joblib.cpu_count()} concurrent jobs."
        )
        print(
            f"Total count of Pacti operations: {nb_contracts20} contracts; {nb_merge20} merges; and {nb_compose20} compositions."
        )

        s = open("space_mission/data/scenarios20.data", "wb")
        pickle.dump(scenarios20, s)
        s.close()
