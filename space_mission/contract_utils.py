"""Helper module for the space mission case study."""
from pacti.terms.polyhedra import PolyhedralContract

from pacti import write_contracts_to_file
from pacti.iocontract import Var
from typing import Optional, List, Tuple, Union
from dataclasses import dataclass
import numpy as np
import pathlib
import operator

from cpuinfo import get_cpu_info
cpu_info = get_cpu_info()
cpu_info_message = f"{cpu_info['brand_raw']} @ {cpu_info['hz_advertised_friendly']} with up to {cpu_info['count']} threads."

tuple2float = Tuple[float, float]

here = pathlib.Path(__file__).parent.resolve()

epsilon = 0

@dataclass(frozen=True, kw_only=True)
class OperationCounts:
    contracts: int
    compositions: int
    merges: int

    def __str__(self) -> str:
        return f"{self.contracts} contracts, {self.compositions} compositions, and {self.merges} merges"
    
@dataclass(frozen=True)
class Schedule:
    scenario: List[tuple2float]
    reqs: np.ndarray
    contract: PolyhedralContract


numeric = Union[int, float]

tuple2 = Tuple[Optional[numeric], Optional[numeric]]


def check_tuple(t: tuple2) -> tuple2float:
    if t[0] is None:
        a = -1.0
    else:
        a = t[0]
    if t[1] is None:
        b = -1.0
    else:
        b = t[1]
    return (a, b)


def bounds(c: PolyhedralContract) -> List[str]:
    bounds=[]
    for v in sorted(c.inputvars, key=operator.attrgetter('name')):
        try:
            b = c.get_variable_bounds(v.name)
            if b[0]:
                low = f"{b[0]:.2f}"
            else:
                low = "None"
            if b[1]:
                high = f"{b[1]:.2f}"
            else:
                high = "None"
            bounds.append(f" input {v.name} in [{low},{high}]")
        except ValueError:
            bounds.append(f" input {v.name} is unsatisfiable")
    for v in sorted(c.outputvars, key=operator.attrgetter('name')):
        try:
            b = c.get_variable_bounds(v.name)
            if b[0]:
                low = f"{b[0]:.2f}"
            else:
                low = "None"
            if b[1]:
                high = f"{b[1]:.2f}"
            else:
                high = "None"
            bounds.append(f"output {v.name} in [{low},{high}]")
        except ValueError:
            bounds.append(f"output {v.name} is unsatisfiable")
    return bounds


def nochange_contract(s: int, name: str) -> PolyhedralContract:
    """
    Constructs a no-change contract between entry/exit variables derived from the name and step index.

    Args:
        s: step index
        name: name of the variable

    Returns:
        A no-change contract.
    """
    return PolyhedralContract.from_string(
        input_vars=[f"{name}{s}_entry"],
        output_vars=[f"{name}{s}_exit"],
        assumptions=[
            f"0 <= {name}{s}_entry",
        ],
        guarantees=[
            f"{name}{s}_exit = {name}{s}_entry",
        ],
    )


def scenario_sequence(
    c1: PolyhedralContract,
    c2: PolyhedralContract,
    variables: list[str],
    c1index: int,
    c2index: Optional[int] = None,
    file_name: Optional[str] = None,
) -> PolyhedralContract:
    """
    Composes c1 with a c2 modified to rename its entry variables according to c1's exit variables

    Args:
        c1: preceding step in the scenario sequence
        c2: next step in the scenario sequence
        variables: list of entry/exit variable names for renaming
        c1index: the step number for c1's variable names
        c2index: the step number for c2's variable names; defaults ti c1index+1 if unspecified

    Returns:
        c1 composed with a c2 modified to rename its c2index-entry variables
        to c1index-exit variables according to the variable name correspondences
        with a post-composition renaming of c1's exit variables to fresh outputs
        according to the variable names.
    """
    if not c2index:
        c2index = c1index + 1
    c2_inputs_to_c1_outputs = [(f"{v}{c2index}_entry", f"{v}{c1index}_exit") for v in variables]
    keep_c1_outputs = [f"{v}{c1index}_exit" for v in variables]
    renamed_c1_outputs = [(f"{v}{c1index}_exit", f"output_{v}{c1index}") for v in variables]

    c2_with_inputs_renamed = c2.rename_variables(c2_inputs_to_c1_outputs)
    c12_with_outputs_kept = c1.compose(c2_with_inputs_renamed, vars_to_keep=keep_c1_outputs)
    c12 = c12_with_outputs_kept.rename_variables(renamed_c1_outputs)

    if file_name:
        write_contracts_to_file(
            contracts=[c1, c2_with_inputs_renamed, c12_with_outputs_kept],
            names=["c1", "c2_with_inputs_renamed", "c12_with_outputs_kept"],
            file_name=file_name,
        )

    return c12


named_contract_t = Tuple[str, PolyhedralContract]

named_contracts_t = List[named_contract_t]

contract_names_t = List[str]


@dataclass(frozen=True)
class FailedMerges:
    current: PolyhedralContract
    merged: contract_names_t
    failed_name: str
    failed_contract: PolyhedralContract


merge_result_t = Union[FailedMerges, PolyhedralContract]

schedule_result_t = Union[FailedMerges, Schedule]

schedule_results_t = Tuple[List[FailedMerges], List[Schedule]]


def perform_merges_seq(c: PolyhedralContract, c_seq: named_contracts_t) -> merge_result_t:
    names: contract_names_t = []
    current: PolyhedralContract = c
    for cn, cc in c_seq:
        try:
            current = current.merge(cc)
            names.append(cn)
        except ValueError:
            return FailedMerges(current, names, cn, cc)
    return current


def aggregate_schedule_results(srs: List[schedule_result_t]) -> schedule_results_t:
    f: List[FailedMerges] = sorted([r for r in srs if isinstance(r, FailedMerges)], key=lambda fm: -len(fm.merged))
    s: List[Schedule] = [r for r in srs if isinstance(r, Schedule)]
    return f, s
