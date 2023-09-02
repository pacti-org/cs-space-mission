from pacti.contracts import PolyhedralIoContract
from pacti_instrumentation.pacti_counters import PactiInstrumentationData
import numpy as np
from contract_utils import *


compose_right_to_left = True

nb_contracts = 0
nb_merge = 0
nb_compose = 0

# epsilon = 1e-6
epsilon = 0


def reset_nb_counts() -> None:
    global nb_contracts
    nb_contracts = 0
    global nb_merge
    nb_merge = 0
    global nb_compose
    nb_compose = 0


def print_counts() -> None:
    print(f"{nb_contracts} contracts; {nb_compose} compositions; {nb_merge} merges.")


# Power viewpoint


# Parameters:
# - s: index of the timeline variables
# - generation: (min, max) rate of battery charge during the task instance
def CHRG_power(s: int, generation: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"soc{s}_entry",  # initial battery SOC
            f"duration_charging{s}",  # variable task duration
        ],
        output_vars=[
            f"soc{s}_exit",  # final battery SOC
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"0 <= duration_charging{s}",
            # Lower and upper bound on entry soc
            f"0 <= soc{s}_entry <= 100.0",
            # Battery should not overcharge
            f"soc{s}_entry + {generation[1]}*duration_charging{s} <= 100",
        ],
        guarantees=[
            # duration*generation(min) <= soc{exit} - soc{entry} <= duration*generation(max)
            f"{generation[0]}*duration_charging{s} <= soc{s}_exit - soc{s}_entry <= {generation[1]}*duration_charging{s}",
            # Battery cannot exceed maximum SOC
            f"soc{s}_exit <= 100",
            # Battery should not completely discharge
            f"0 <= soc{s}_exit",
        ],
    )
    return spec

    # Parameters:


def power_consumer(s: int, task: str, consumption: tuple[float, float]) -> PolyhedralIoContract:
    """A contract for discharging the battery during the task instance.

    Args:
        s (int): step index
        task (str): task name
        consumption (tuple[float, float]): min,max range of battery discharge during the task instance

    Returns:
        PolyhedralIoContract: The discharge contract
    """
    global nb_contracts
    nb_contracts += 1
    return PolyhedralIoContract.from_strings(
        input_vars=[
            f"soc{s}_entry",  # initial battery SOC
            f"duration_{task}{s}",  # variable task duration
        ],
        output_vars=[
            f"soc{s}_exit",  # final battery SOC
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"0 <= duration_{task}{s}",
            # Upper bound on entry soc
            f"soc{s}_entry <= 100.0",
            # Lower bound on entry soc
            f"0 <= soc{s}_entry",
            # Battery has enough energy for worst-case consumption throughout the task instance
            f"soc{s}_entry >= {consumption[1]}*duration_{task}{s}",
        ],
        guarantees=[
            # The state of charge decrease, soc{entry} - soc{exit}, is bounded by the duration * min/max consumption rate
            f"{consumption[0]}*duration_{task}{s} <= soc{s}_entry - soc{s}_exit <= {consumption[1]}*duration_{task}{s}",
            # Battery cannot exceed maximum SOC
            f"soc{s}_exit <= 100",
            # Battery should not completely discharge
            f"0 <= soc{s}_exit",
        ],
    )


power_variables = ["soc"]


def generate_power_scenario(
    s: int,
    dsn_cons: tuple[float, float],
    chrg_gen: tuple[float, float],
    sbo_cons: tuple[float, float],
    tcmh_cons: tuple[float, float],
    tcmdv_cons: tuple[float, float],
    rename_outputs: bool = False,
) -> PolyhedralIoContract:
    global nb_compose
    nb_compose += 4  # scenario_sequence

    s1 = power_consumer(s=s, task="dsn", consumption=dsn_cons)
    s2 = CHRG_power(s=s + 1, generation=chrg_gen)
    s3 = power_consumer(s=s + 2, task="sbo", consumption=sbo_cons)
    s4 = power_consumer(s=s + 3, task="tcm_h", consumption=tcmh_cons)
    s5 = power_consumer(s=s + 4, task="tcm_dv", consumption=tcmdv_cons)

    if compose_right_to_left:
        steps2 = scenario_sequence(c1=s4, c2=s5, variables=power_variables, c1index=s + 3)
        steps3 = scenario_sequence(c1=s3, c2=steps2, variables=power_variables, c1index=s + 2)
        steps4 = scenario_sequence(c1=s2, c2=steps3, variables=power_variables, c1index=s + 1)
        steps5 = scenario_sequence(c1=s1, c2=steps4, variables=power_variables, c1index=s)
    else:
        steps2 = scenario_sequence(c1=s1, c2=s2, variables=power_variables, c1index=s)
        steps3 = scenario_sequence(c1=steps2, c2=s3, variables=power_variables, c1index=s + 1)
        steps4 = scenario_sequence(c1=steps3, c2=s4, variables=power_variables, c1index=s + 2)
        steps5 = scenario_sequence(c1=steps4, c2=s5, variables=power_variables, c1index=s + 3)

    if rename_outputs:
        return steps5.rename_variables([(f"soc{s+4}_exit", f"output_soc{s+4}")])
    else:
        return steps5


# Science & communication viewpoint


# - s: start index of the timeline variables
# - speed: (min, max) downlink rate during the task instance
def DSN_data(s: int, speed: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"d{s}_entry",  # initial data volume
            f"duration_dsn{s}",  # variable task duration
        ],
        output_vars=[
            f"d{s}_exit",  # final data volume
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"duration_dsn{s} >= 0",
            # downlink data lower,upper bound
            f"0 <= d{s}_entry <= 100",
        ],
        guarantees=[
            # duration*speed(min) <= d{entry} - d{exit} <= duration*speed(max)
            f"{speed[0]}*duration_dsn{s} <= d{s}_entry - d{s}_exit <= {speed[1]}*duration_dsn{s}",
            # downlink transmits at most all the data.
            f"d{s}_exit >= 0",
        ],
    )
    return spec


# Parameters:
# - s: start index of the timeline variables
# - generation: (min, max) rate of small body observations during the task instance
def SBO_science_storage(s: int, generation: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"d{s}_entry",  # initial data storage volume
            f"duration_sbo{s}",  # knob variable for SBO duration
        ],
        output_vars=[
            f"d{s}_exit",  # final data storage volume
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"duration_sbo{s} >= 0",
            # There is enough data storage available
            f"d{s}_entry + {generation[1]}*duration_sbo{s} <= 100",
            # downlink data lower bound
            f"0 <= d{s}_entry",
        ],
        guarantees=[
            # The increase in data, d{exit} - d{entry}, has a lower/upper bound as the min/max generation rate * duration
            f"{generation[0]}*duration_sbo{s} <= d{s}_exit - d{s}_entry <= {generation[1]}*duration_sbo{s}",
            # Data volume cannot exceed the available storage capacity
            f"d{s}_exit <= 100",
        ],
    )
    return spec


def SBO_science_comulative(s: int, generation: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"c{s}_entry",  # initial cumulative data volume
            f"duration_sbo{s}",  # knob variable for SBO duration
        ],
        output_vars=[
            f"c{s}_exit",  # final cumulative data volume
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"duration_sbo{s} >= 0",
            # cumulative data lower bound
            f"c{s}_entry >= 0",
        ],
        guarantees=[
            # The increase in cummulated data, c{exit} - c{entry}, has a lower/upper bound as the min/max generation rate * duration
            f"{generation[0]}*duration_sbo{s} <= c{s}_exit - c{s}_entry <= {generation[1]}*duration_sbo{s}",
        ],
    )
    return spec


science_variables = ["d", "c"]


def generate_science_scenario(
    s: int, dsn_speed: tuple[float, float], sbo_gen: tuple[float, float], rename_outputs: bool = False
) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 7  # nochange_contract
    global nb_merge
    nb_merge += 5
    global nb_compose
    nb_compose += 4  # scenario_sequence

    s1 = DSN_data(s=s, speed=dsn_speed).merge(nochange_contract(s=s, name="c"))
    s2 = nochange_contract(s=s + 1, name="d").merge(nochange_contract(s=s + 1, name="c"))
    s3 = SBO_science_storage(s=s + 2, generation=sbo_gen).merge(SBO_science_comulative(s=s + 2, generation=sbo_gen))
    s4 = nochange_contract(s=s + 3, name="d").merge(nochange_contract(s=s + 3, name="c"))
    s5 = nochange_contract(s=s + 4, name="d").merge(nochange_contract(s=s + 4, name="c"))

    if compose_right_to_left:
        steps2 = scenario_sequence(c1=s4, c2=s5, variables=science_variables, c1index=s + 3)
        steps3 = scenario_sequence(c1=s3, c2=steps2, variables=science_variables, c1index=s + 2)
        steps4 = scenario_sequence(c1=s2, c2=steps3, variables=science_variables, c1index=s + 1)
        steps5 = scenario_sequence(c1=s1, c2=steps4, variables=science_variables, c1index=s)
    else:
        steps2 = scenario_sequence(c1=s1, c2=s2, variables=science_variables, c1index=s)
        steps3 = scenario_sequence(c1=steps2, c2=s3, variables=science_variables, c1index=s + 1)
        steps4 = scenario_sequence(c1=steps3, c2=s4, variables=science_variables, c1index=s + 2)
        steps5 = scenario_sequence(c1=steps4, c2=s5, variables=science_variables, c1index=s + 3)

    if rename_outputs:
        return steps5.rename_variables(
            [
                (f"d{s+3}_exit", f"output_d{s+3}"),
                (f"c{s+3}_exit", f"output_c{s+3}"),
                (f"d{s+4}_exit", f"output_d{s+4}"),
                (f"c{s+4}_exit", f"output_c{s+4}"),
            ]
        )
    else:
        return steps5


# Verify we get the same contract as the notebook...
# print(generate_science_scenario(dsn_speed=(5.2, 5.5), sbo_gen=(3.0, 4.0)))

# Navigation viewpoint


def uncertainty_generating_nav(s: int, noise: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"u{s}_entry",  # initial trajectory estimation uncertainty
            f"r{s}_entry",  # initial relative trajectory distance
        ],
        output_vars=[
            f"u{s}_exit",  # final trajectory estimation uncertainty
            f"r{s}_exit",  # final relative trajectory distance
        ],
        assumptions=[
            # 0 <= u{s}_entry <= 100
            f"0 <= u{s}_entry",
            # f" u{s}_entry <= 100",
            # 0 <= r{s}_entry <= 100
            f"0 <= r{s}_entry",
            # f" r{s}_entry <= 100",
        ],
        guarantees=[
            # The increase in uncertainty, u{exit} - u{entry}, has lower/upper bound in the min/max noise.
            f"{noise[0]} <= u{s}_exit - u{s}_entry <= {noise[1]}",
            # no change to relative trajectory distance
            # NFR
            f"| r{s}_exit - r{s}_entry | <= {epsilon}",
            # Lower-bound on the trajectory estimation uncertainty
            f"0 <= u{s}_exit",
        ],
    )
    return spec


# Parameters:
# - s: start index of the timeline variables
# - improvement: rate of trajectory estimation uncertainty improvement during the task instance
def SBO_nav_uncertainty(s: int, improvement: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"u{s}_entry",  # initial trajectory uncertainty
            f"duration_sbo{s}",  # knob variable for SBO duration
        ],
        output_vars=[
            f"u{s}_exit",  # final trajectory uncertainty
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"0 <= duration_sbo{s}",
            f"0 <= u{s}_entry",
            # Upper-bound on the trajectory estimation uncertainty
            # f"u{s}_entry <= 100",
        ],
        guarantees=[
            # upper bound u{s}_exit <= 100
            # f"u{s}_exit <= 100",
            # duration*improvement(min) <= u{entry} - u{exit} <= duration*improvement(max)
            f"{improvement[0]}*duration_sbo{s} <= u{s}_entry - u{s}_exit <= {improvement[1]}*duration_sbo{s}",
            # Lower-bound on the trajectory estimation uncertainty
            f"0 <= u{s}_exit",
        ],
    )
    return spec


def TCM_navigation_deltav_uncertainty(s: int, noise: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"u{s}_entry",  # initial trajectory estimation uncertainty
            f"duration_tcm_dv{s}",  # knob variable for TCM deltav duration
        ],
        output_vars=[
            f"u{s}_exit",  # final trajectory estimation uncertainty
        ],
        assumptions=[
            # Task has a positive scheduled duration
            f"0 <= duration_tcm_dv{s}",
            # 0 <= u{s}_entry <= 100
            f"0 <= u{s}_entry",
            # f" u{s}_entry <= 100",
        ],
        guarantees=[
            # upper bound u{s}_exit <= 100
            # f"u{s}_exit <= 100",
            # noise(min) <= u{exit} - u{entry} <= noise(max)
            f"{noise[0]} duration_tcm_dv{s} <= u{s}_exit - u{s}_entry <= {noise[1]} duration_tcm_dv{s}",
            # Lower-bound on the trajectory estimation uncertainty
            f"0 <= u{s}_exit",
        ],
    )
    return spec


def TCM_navigation_deltav_progress(s: int, progress: tuple[float, float]) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 1
    spec = PolyhedralIoContract.from_strings(
        input_vars=[
            f"r{s}_entry",  # initial trajectory relative distance
            f"duration_tcm_dv{s}",  # knob variable for TCM deltav duration
        ],
        output_vars=[
            f"r{s}_exit",  # final trajectory relative distance
        ],
        assumptions=[
            # upper bound on trajectory relative distance
            f"0 <= r{s}_entry",
            # f"r{s}_entry <= 100",
        ],
        guarantees=[
            # upper bound r{s}_exit <= 100
            # f"r{s}_exit <= 100",
            # duration*improvement(min) <= r{entry} - r{exit} <= duration*improvement(max)
            f"{progress[0]}*duration_tcm_dv{s} <= r{s}_entry - r{s}_exit <= {progress[1]}*duration_tcm_dv{s}",
            # lower bound on trajectory relative distance
            f"0 <= r{s}_exit",
        ],
    )
    return spec


navigation_variables = ["u", "r"]


def generate_navigation_scenario(
    s: int,
    dsn_noise: tuple[float, float],
    chrg_noise: tuple[float, float],
    sbo_imp: tuple[float, float],
    tcm_dv_noise: tuple[float, float],
    tcm_dv_progress: tuple[float, float],
    rename_outputs: bool = False,
) -> PolyhedralIoContract:
    global nb_contracts
    nb_contracts += 3  # nochange_contract
    global nb_merge
    nb_merge += 3
    global nb_compose
    nb_compose += 4  # scenario_sequence
    s1 = uncertainty_generating_nav(s=s, noise=dsn_noise)
    s2 = uncertainty_generating_nav(s=s + 1, noise=chrg_noise)
    s3 = SBO_nav_uncertainty(s=s + 2, improvement=sbo_imp).merge(nochange_contract(s=s + 2, name="r"))
    s4 = nochange_contract(s=s + 3, name="u").merge(nochange_contract(s=s + 3, name="r"))
    s5 = TCM_navigation_deltav_uncertainty(s=s + 4, noise=tcm_dv_noise).merge(
        TCM_navigation_deltav_progress(s=s + 4, progress=tcm_dv_progress)
    )

    if compose_right_to_left:
        steps2 = scenario_sequence(c1=s4, c2=s5, variables=navigation_variables, c1index=s + 3)
        steps3 = scenario_sequence(c1=s3, c2=steps2, variables=navigation_variables, c1index=s + 2)
        steps4 = scenario_sequence(c1=s2, c2=steps3, variables=navigation_variables, c1index=s + 1)
        steps5 = scenario_sequence(c1=s1, c2=steps4, variables=navigation_variables, c1index=s)
    else:
        steps2 = scenario_sequence(c1=s1, c2=s2, variables=navigation_variables, c1index=s)
        steps3 = scenario_sequence(c1=steps2, c2=s3, variables=navigation_variables, c1index=s + 1)
        steps4 = scenario_sequence(c1=steps3, c2=s4, variables=navigation_variables, c1index=s + 2)
        steps5 = scenario_sequence(c1=steps4, c2=s5, variables=navigation_variables, c1index=s + 3)

    if rename_outputs:
        return steps5.rename_variables(
            [
                (f"u{s+3}_exit", f"output_u{s+3}"),
                (f"r{s+3}_exit", f"output_r{s+3}"),
                (f"u{s+4}_exit", f"output_u{s+4}"),
                (f"r{s+4}_exit", f"output_r{s+4}"),
            ]
        )
    else:
        return steps5


def make_range(mean: float, dev: float) -> tuple2float:
    delta = mean * dev
    return (mean - delta, mean + delta)


def make_scenario(
    s: int, means: np.ndarray, devs: np.ndarray, rename_outputs: bool = False
) -> Tuple[List[tuple2float], PolyhedralIoContract]:
    global nb_merge
    nb_merge += 2

    ranges = [make_range(m, d) for (m, d) in zip(means, devs)]
    scenario_pwr = generate_power_scenario(
        s,
        dsn_cons=ranges[0],
        chrg_gen=ranges[1],
        sbo_cons=ranges[2],
        tcmh_cons=ranges[3],
        tcmdv_cons=ranges[4],
        rename_outputs=rename_outputs,
    )

    scenario_sci = generate_science_scenario(s, dsn_speed=ranges[5], sbo_gen=ranges[6], rename_outputs=rename_outputs)

    scenario_nav = generate_navigation_scenario(
        s,
        dsn_noise=ranges[7],
        chrg_noise=ranges[8],
        sbo_imp=ranges[9],
        tcm_dv_noise=ranges[10],
        tcm_dv_progress=ranges[11],
        rename_outputs=rename_outputs,
    )

    return (ranges, scenario_pwr.merge(scenario_sci).merge(scenario_nav))


def generate_5step_scenario(
    mean_dev: Tuple[np.ndarray, np.ndarray]
) -> Tuple[PactiInstrumentationData, List[tuple2float], PolyhedralIoContract]:
    return (PactiInstrumentationData().update_counts(),) + make_scenario(1, mean_dev[0], mean_dev[1], True)


all_variables = power_variables + science_variables + navigation_variables


def generate_20step_scenario(
    mean_dev: Tuple[np.ndarray, np.ndarray]
) -> Tuple[PactiInstrumentationData, List[tuple2float], PolyhedralIoContract]:
    global nb_compose
    nb_compose += 3  # scenario_sequence

    ranges, l1 = make_scenario(s=1, means=mean_dev[0], devs=mean_dev[1], rename_outputs=False)
    _, l2 = make_scenario(s=6, means=mean_dev[0], devs=mean_dev[1], rename_outputs=False)
    _, l3 = make_scenario(s=11, means=mean_dev[0], devs=mean_dev[1], rename_outputs=False)
    _, l4 = make_scenario(s=16, means=mean_dev[0], devs=mean_dev[1], rename_outputs=True)

    if compose_right_to_left:
        l34 = scenario_sequence(c1=l3, c2=l4, variables=all_variables, c1index=15)
        l234 = scenario_sequence(c1=l2, c2=l34, variables=all_variables, c1index=10)
        l1234 = scenario_sequence(c1=l1, c2=l234, variables=all_variables, c1index=5)
    else:
        l12 = scenario_sequence(c1=l1, c2=l2, variables=all_variables, c1index=5)
        l123 = scenario_sequence(c1=l12, c2=l3, variables=all_variables, c1index=10)
        l1234 = scenario_sequence(c1=l123, c2=l4, variables=all_variables, c1index=15)

    return (PactiInstrumentationData().update_counts(), ranges, l1234)
