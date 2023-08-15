from pacti.terms.polyhedra import PolyhedralContract
from typing import Tuple
from utils import (
    contract_shift,
    get_numerical_bounds,
    nochange_contract,
    plot_steps,
    scenario_sequence,
    tuple2float,
)
import time
from matplotlib.figure import Figure

from functools import partial
from typing import List, Tuple
from functools import reduce
from p_tqdm import p_map, p_umap

def meas_nav_error(
    step: int, mu: float
) -> PolyhedralContract:
    """Measurement function in the navigation domain.
    
    Args:
        step (int): sequence step index.
        mu (float): maximum range of measurement uncertainty, mu,
                    that applies proportionally to relative distance.

    Returns:
        PolyhedralContract: Navigation measurement sequence step contract.
    """

    # step duration
    duration: str = f"duration{step}"

    # time
    t_entry: str = f"t{step}_entry"
    t_exit: str = f"t{step}_exit"

    # true relative trajectory distance
    trtd_entry: str = f"trtd{step}_entry"
    trtd_exit: str = f"trtd{step}_exit"

    # true trajectory intercept distance
    ttid_entry: str = f"ttid{step}_entry"
    ttid_exit: str = f"ttid{step}_exit"

    # trajectory error
    error: str = f"error{step}_exit"

    return PolyhedralContract.from_string(
        input_vars=[duration, t_entry, trtd_entry, ttid_entry],
        output_vars=[t_exit, trtd_exit, ttid_exit, error],
        assumptions=[
            # The task has a positive scheduled duration.
            f"0 <= {duration}",
            # The time of entry must be positive.
            f"0 <= {t_entry}",
            # trtd bounds
            # f"0 <= {trtd_entry} <= 100",
        ],
        guarantees=[
            # No change to the trtp
            f"{trtd_exit} = {trtd_entry}",
            # task duration determines time of exit
            f"{t_exit} = {t_entry} + {duration}",
            # The absolute magnitude of the error has an upper bound 
            # proportional to the true relative trajectory progress.
            f"|{error}| <= {mu}*{trtd_entry}",
        ],
    )

def estimate_nav(step: int) -> PolyhedralContract:
    """Calculate delta-v maneuver to reduce the relative trajectory distance.

    Args:
        step (int): sequence step index.

    Returns:
        PolyhedralContract: relative trajectory navigation estimate
                            from nav measurement errors
    """
    # step duration
    duration: str = f"duration{step}"

    # time
    t_entry: str = f"t{step}_entry"
    t_exit: str = f"t{step}_exit"

    # true relative trajectory distance
    trtd_entry: str = f"trtd{step}_entry"
    trtd_exit: str = f"trtd{step}_exit"

    # estimated relative trajectory distance
    ertd: str = f"ertd{step}_exit"

    # trajectory error
    error: str = f"error{step}_entry"
    
    return PolyhedralContract.from_string(
        input_vars=[duration, t_entry, trtd_entry, error],
        output_vars=[t_exit, trtd_exit, ertd],
        assumptions=[
            # The task has a positive scheduled duration.
            f"0 <= {duration}",
            # The time of entry must be positive.
            f"0 <= {t_entry}",
            # trtd bounds
            # f"0 <= {trtd_entry} <= 100",
        ],
        guarantees=[
            # No change to the trtp
            f"{trtd_exit} = {trtd_entry}",
            # task duration determines time of exit
            f"{t_exit} = {t_entry} + {duration}",
            # The absolute magnitude of the error has an upper bound 
            # proportional to the true relative trajectory progress.
            f"{ertd} = {error} + {trtd_entry}",
        ],
    )

def calculate_dv(step: int, gain: Tuple[float, float], max_dv: float) -> PolyhedralContract:
    """Estimate mission design navigation trajectory and delta-v correction

    Args:
        step (int): sequence step index.
        gain (Tuple[float, float]): range of delta-v as a proportional gain of
                                    estimated relative trajectory distance. 
        max_dv (float): maximum delta-v capability.

    Returns:
        PolyhedralContract: relative trajectory navigation estimate
                            from nav measurement errors with calculated delta-v maneuver
    """
    # step duration
    duration: str = f"duration{step}"

    # time
    t_entry: str = f"t{step}_entry"
    t_exit: str = f"t{step}_exit"

    # estimated relative trajectory distance
    ertd: str = f"ertd{step}_entry"
    
    # trajectory correction
    dv: str = f"dv{step}_exit"
    
    return PolyhedralContract.from_string(
        input_vars=[duration, t_entry, ertd],
        output_vars=[t_exit, dv],
        assumptions=[
            # The task has a positive scheduled duration.
            f"0 <= {duration}",
            # The time of entry must be positive.
            f"0 <= {t_entry}",
        ],
        guarantees=[
            # task duration determines time of exit
            f"{t_exit} = {t_entry} + {duration}",
            
            f"{gain[0]}*{ertd} <= {dv} <= {gain[1]}*{ertd}",
            
            f"0 <= {dv} <= {max_dv}"
        ],
    )

def dv_maneuver(step: int, me: Tuple[float, float]) -> PolyhedralContract:
    """Apply a delta-v maneuver

    Args:
        step (int): sequence step index.
        me (Tuple[float, float]): min/max range of maneuver execution error proportional to the delta-v.

    Returns:
        PolyhedralContract: Updated true relative trajectory distance with delta-v applied up to maneuver execution error.
    """
    
    # step duration
    duration: str = f"duration{step}"

    # time
    t_entry: str = f"t{step}_entry"
    t_exit: str = f"t{step}_exit"
    
    # true relative trajectory distance
    trtd_entry: str = f"trtd{step}_entry"
    trtd_exit: str = f"trtd{step}_exit"

    # trajectory correction
    dv: str = f"dv{step}_entry"

    return PolyhedralContract.from_string(
        input_vars=[duration, t_entry, trtd_entry, dv],
        output_vars=[t_exit, trtd_exit],
        assumptions=[
            # The task has a positive scheduled duration.
            f"0 <= {duration}",
            # The time of entry must be positive.
            f"0 <= {t_entry}",
        ],
        guarantees=[
            # task duration determines time of exit
            f"{t_exit} = {t_entry} + {duration}",
            
            f"{me[0]}*{dv} <= {trtd_entry} - {trtd_exit} <= {me[1]}*{dv}",
        ],
    )


class NAVLoop:
    """Navigation loop for relative trajectory distance."""

    def __init__(
        self,
        step: int,
        mu: float,
        gain: Tuple[float, float],
        max_dv: float,
        me: Tuple[float, float],
    ):
        """Construct a contract corresponding to the unrolling of one iteration around 
        functions involved in the navigation feedback loop: Meas, OD, MDNav, and TCM.

        Args:
            step (int): starting step for the sequence
            mu (float): maximum range of measurement uncertainty, mu,
                        that applies proportionally to relative distance.
            gain (Tuple[float, float]): range of delta-v as a proportional gain of
                                        estimated relative trajectory distance.
            max_dv (float): maximum delta-v capability.
            me (Tuple[float, float]): min/max range of maneuver execution error proportional to the delta-v.
        """
        self.meas: PolyhedralContract = meas_nav_error(step, mu).merge(
            nochange_contract(step, name="ttid")
        )
        self.od: PolyhedralContract = estimate_nav(step + 1).merge(
            nochange_contract(step + 1, name="ttid")
        )
        self.mdnav: PolyhedralContract = calculate_dv(step + 2, gain, max_dv).merge(
            nochange_contract(step + 2, name="trtd")
        ).merge(
            nochange_contract(step + 2, name="ttid")
        )
        self.tcm: PolyhedralContract = dv_maneuver(step + 3, me).merge(
            nochange_contract(step + 3, name="ttid")
        )

        self.steps34: PolyhedralContract = scenario_sequence(
            c1=self.mdnav, c2=self.tcm, variables=["dv", "t", "trtd", "ttid"], c1index=step + 2
        )
        self.steps234: PolyhedralContract = scenario_sequence(
            c1=self.od,
            c2=self.steps34,
            variables=["ertd", "t", "trtd", "ttid"],
            c1index=step + 1,
        )
        self.steps1234: PolyhedralContract = scenario_sequence(
            c1=self.meas,
            c2=self.steps234,
            variables=["error", "t", "trtd", "ttid"],
            c1index=step,
        )


class NAVLoopUnrolling:
    """Unroll up to a fixed number of iterations of the navigation feedback loop
    to determine whether the mission is achievable within that number of iterations."""

    def __init__(
        self,
        min_iterations: int,
        max_iterations: int,
        mu: float,
        gain: Tuple[float, float],
        max_dv: float,
        me: Tuple[float, float],
    ) -> None:
        if not (0 <= min_iterations and min_iterations < max_iterations):
            raise ValueError(
                f"min iterations must be greater than zero and less than max iterations; got: {min_iterations=}, {max_iterations=}"
            )

        # Create a partial function with mu, gain, max_dv and me pre-filled
        partial_create_NAVLoop = partial(
            NAVLoopUnrolling.create_NAVLoop, mu=mu, gain=gain, max_dv=max_dv, me=me
        )

        # Create NAVLoop objects in parallel
        self.loops: List[NAVLoop] = p_map(partial_create_NAVLoop, range(max_iterations))

        # Create arguments for unroll method
        args_for_unroll: List[List[Tuple[int, PolyhedralContract]]] = [
            [(i, loop.steps1234) for i, loop in enumerate(self.loops[: j + 1])]
            for j in range(min_iterations, max_iterations)
        ]

        # Parallelized map with progress bar
        self.sequences: List[Tuple[int, PolyhedralContract]] = list(
            p_umap(lambda args: self.unroll(args), args_for_unroll)
        )

    @staticmethod
    def create_NAVLoop(
        i: int,
        mu: float,
        gain: Tuple[float, float],
        max_dv: float,
        me: Tuple[float, float],
    ) -> NAVLoop:
        return NAVLoop(step=1 + 4 * i, mu=mu, gain=gain, max_dv=max_dv, me=me)

    @staticmethod
    def unroll(
        loops: List[Tuple[int, PolyhedralContract]]
    ) -> Tuple[int, PolyhedralContract]:
        return reduce(NAVLoopUnrolling.sequence_compose, reversed(loops))

    @staticmethod
    def sequence_compose(
        a: Tuple[int, PolyhedralContract], b: Tuple[int, PolyhedralContract]
    ) -> Tuple[int, PolyhedralContract]:
        bindex: int = 4 + 4 * b[0]
        aindex: int = max(a[0], 4 + bindex)
        return (
            aindex,
            scenario_sequence(
                c1=b[1], c2=a[1], variables=["t", "trtd", "ttid"], c1index=bindex
            ),
        )

    def show_bounds(self, index: int, var: str, title: str, text: str, nth_tick: int) -> Figure:
        (n, c) = self.sequences[index]
        print(f"generating bounds plot for a sequence of {n=} steps...")
        sn = ["initial"]
        for i in range( n // 4):
            sn = sn + [f"meas{i}", f"od{i}", f"mdnav{i}", f"tcm{i}"]

        last_bounds: tuple2float = get_numerical_bounds(c=c, var=f"{var}{n}_exit")
        sb: List[tuple2float] = (
            [get_numerical_bounds(c=c, var=f"{var}1_entry")]
            + [
                get_numerical_bounds(c=c, var=f"output_{var}{i}")
                for i in range(1, n)
            ]
            + [last_bounds]
        )
        text = text + f"\n{len(c.inputvars)} input variables\n{len(c.outputvars)} output variables\n{len(c.a.terms)} assumptions\n{len(c.g.terms)} constraints"
        text = text + f"\n{n} sequence steps\nbounds({var}{n}_exit)=[{last_bounds[0]:.3g},{last_bounds[1]:.3g}]"
        return plot_steps(
            step_bounds=sb,
            step_names=sn,
            ylabel=var,
            title=title,
            text=text,
            nth_tick=nth_tick
        )

class NAVScenario:
    def __init__(
        self,
        iterations: int,
        mu: float,
        gain: Tuple[float, float],
        max_dv: float,
        me: Tuple[float, float],
        variables: List[str]
    ) -> None:
        if not (0 <= iterations):
            raise ValueError(
                f"iterations must be greater than zero; got: {iterations=}"
            )
        l1 = NAVLoop(step=1, mu=mu, gain=gain, max_dv=max_dv, me=me)
        l2 = NAVLoop(step=5, mu=mu, gain=gain, max_dv=max_dv, me=me)
        current = scenario_sequence(c1=l1.steps1234, c2=l2.steps1234, variables=variables, c1index=4)
        self.contracts: List[Tuple[int, PolyhedralContract, floa, float]] = []
        length: int = 2
        for _ in range(iterations):
            length = length+1
            ta = time.time()
            current_shift: PolyhedralContract = contract_shift(c=current, offset=4)
            tb = time.time()
            current: PolyhedralContract = scenario_sequence(c1=l1.steps1234, c2=current_shift, variables=variables, c1index=4)
            tc = time.time()
            tuple: Tuple[int, PolyhedralContract, float, float] = (length, current, tb - ta, tc - tb)
            self.contracts.append(tuple)
           