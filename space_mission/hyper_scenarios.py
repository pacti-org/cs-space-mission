import time
from pacti.terms.polyhedra import PolyhedralContract
from pacti_instrumentation.pacti_counters import summarize_instrumentation_data
import numpy as np
from contract_utils import *
from generators import *

from typing import Tuple

from p_tqdm import p_umap

from scipy.stats import qmc

import pickle

run5 = True
run20 = True

# Hyperparameter ranges
l_bounds = [
    2.0,  # power: min dns cons
    3.0,  # power: min chrg gen
    0.1,  # power: min sbo cons
    0.2,  # power: min tcm_h cons
    0.1,  # power: min tcm_dv cons
    0.3,  # science: min dsn speed
    2.0,  # science: min sbo gen
    1.0,  # nav: min dsn noise
    0.8,  # nav: min chrg noise
    -0.3,  # nav: min sbo imp
    1.0,  # nav: min tcm_dv noise
    0.3,  # nav: min tcm_dv progress
]
u_bounds = [
    2.5,  # power: max dns cons
    6.0,  # power: max chrg gen
    0.4,  # power: max sbo cons
    1.0,  # power: max tcm_h cons
    0.4,  # power: max tcm_dv cons
    0.7,  # science: max dsn speed
    5.0,  # science: max sbo gen
    1.5,  # nav: max dsn noise
    1.5,  # nav: max chrg noise
    0.8,  # nav: max sbo imp
    2.0,  # nav: max tcm_dv noise
    0.8,  # nav: max tcm_dv progress
]

mean_sampler = qmc.LatinHypercube(d=len(l_bounds))
dev_sampler = qmc.LatinHypercube(d=len(l_bounds))

if run5:
    n5 = 100
    mean_sample5: np.ndarray = mean_sampler.random(n=n5)
    scaled_mean_sample5: np.ndarray = qmc.scale(sample=mean_sample5, l_bounds=l_bounds, u_bounds=u_bounds)
    dev_sample5: np.ndarray = dev_sampler.random(n=n5)

    ta = time.time()
    results: List[Tuple[PactiInstrumentationData, List[tuple2float], PolyhedralContract]] = p_umap(generate_5step_scenario, list(zip(scaled_mean_sample5, dev_sample5)))
    tb = time.time()

    stats = summarize_instrumentation_data([result[0] for result in results])
    scenarios5 = [result[1:3] for result in results if result[1]]
    print(
        f"Generated {len(scenarios5)} hyperparameter variations of the 5-step scenario in {tb-ta} seconds.\n"
        f"Running on {cpu_info_message}\n"
        f"{stats.stats()}"
    )
    s = open("space_mission/scenarios5.data", "wb")
    pickle.dump(scenarios5, s)
    s.close()

if run20:
    n20 = 100
    # n20 = 100
    # n20 = 50
    mean_sample20: np.ndarray = mean_sampler.random(n=n20)
    scaled_mean_sample20: np.ndarray = qmc.scale(sample=mean_sample20, l_bounds=l_bounds, u_bounds=u_bounds)
    dev_sample20: np.ndarray = dev_sampler.random(n=n20)

    ta = time.time()
    results: List[Tuple[PactiInstrumentationData, List[tuple2float], PolyhedralContract]] = p_umap(generate_20step_scenario, list(zip(scaled_mean_sample20, dev_sample20)))
    tb = time.time()

    stats = summarize_instrumentation_data([result[0] for result in results])
    scenarios20 = [result[1:3] for result in results if result[1]]
    print(
        f"Generated {len(scenarios20)} hyperparameter variations of the 20-step scenario in {tb-ta} seconds.\n"
        f"Running on {cpu_info_message}\n"
        f"{stats.stats()}"
    )
    s = open("space_mission/scenarios20.data", "wb")
    pickle.dump(scenarios20, s)
    s.close()
