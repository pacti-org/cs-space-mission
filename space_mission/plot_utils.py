from matplotlib.backend_bases import Event
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from pacti.iocontract import Var
from pacti.terms.polyhedra import PolyhedralContract, PolyhedralTermList
from pacti.terms.polyhedra.plots import plot_guarantees
from typing import Dict, List, Tuple, Union
from contract_utils import bound

numeric = Union[int, float]


def plot_steps(
    step_bounds: List[Tuple[float, float]], step_names: List[str], ylabel: str, title: str, text: str, nth_tick: int = 1
) -> Figure:
    """
    Create a two-panel plot (two subplots) where the left panel displays a filled polygon representing the input data,
    and the right panel displays some text.

    Args:
        step_bounds:
            A list of tuples, each containing two float values representing the lower and upper bounds of a step.
        step_names:
            A list of strings representing the names of the steps.
        ylabel:
            A string representing the label for the y-axis.
        title:
            A string representing the title of the plot.
        text:
            A string representing the text to be displayed in the right panel.
        nth_tick:
            Show step names at every nth tick

    Returns:
        A two-panel plot figure.
    """
    assert nth_tick >= 1
    assert nth_tick < len(step_names)

    vertices = []
    N = len(step_bounds)
    assert N == len(step_names)
    for i in range(N):
        vertices.append((i + 1, step_bounds[i][0]))
    for i in range(N):
        vertices.append((N - i, step_bounds[N - 1 - i][1]))
    x, y = zip(*vertices)

    fig = plt.figure()
    ax1: Axes = fig.add_subplot(1, 2, 1, aspect="auto")
    ax1.set_ylim(0, 120)

    ax1.set_xticks(range(1, N + 1)[::nth_tick], step_names[::nth_tick], rotation=90, ha="right")

    plt.title(title)
    plt.xlabel("Sequence step")
    plt.ylabel(ylabel)
    plt.fill(x, y, facecolor="deepskyblue")

    ax2 = fig.add_subplot(1, 2, 2, aspect="auto")
    # Build a rectangle in axes coords
    left, width = 0, 1
    bottom, height = 0, 1
    right = left + width
    top = bottom + height
    p = plt.Rectangle((left, bottom), width, height, fill=False)
    p.set_transform(ax2.transAxes)
    p.set_clip_on(False)
    ax2.add_patch(p)

    ax2.text(
        x=0,
        y=0.5 * (bottom + top),
        s=text,
        horizontalalignment="left",
        verticalalignment="center",
        transform=ax2.transAxes,
        fontdict={"family": "monospace", "size": 8},
    )
    ax2.set_axis_off()

    return fig

def get_bounds(ptl: PolyhedralTermList, var: str) -> tuple[str, str]:
    try:
        min = f"{ptl.optimize(objective={Var(var): 1}, maximize=False):.2f}"
    except ValueError:
        min = "unknown"
    try:
        max = f"{ptl.optimize(objective={Var(var): 1}, maximize=True):.2f}"
    except ValueError:
        max = "unknown"

    return min, max

def calculate_output_bounds_for_input_value(ptl: PolyhedralTermList, inputs: Dict[Var, float], output: Var) -> tuple[str,str]:
    return get_bounds(ptl.evaluate(inputs).simplify(), output.name)

# Add a callback function for the mouse click event
def on_hover(ptl: PolyhedralTermList, x_var: Var, y_var: Var, fig: Figure, ax: Axes, event: Event) -> None:
    if event.inaxes == ax:
        x_coord = event.xdata
        try:
            y_min, y_max = calculate_output_bounds_for_input_value(ptl, {x_var: x_coord}, y_var)
            ax.set_title(f"@ {x_var.name}={x_coord:.2f}\n{y_min} <= {y_var.name} <= {y_max}")
        except ValueError as e:
            print(f"Contract guarantee hover ValueError:\n{e}")
            ax.set_title(f"@ {x_var.name}={x_coord:.2f}\nValueError (see message below)")
        fig.canvas.draw_idle()

def plot_guarantees_with_bounds_hover(
    contract: PolyhedralContract,
    x_var: Var,
    y_var: Var,
    var_values: Dict[Var, numeric],
    x_lims: Tuple[numeric, numeric],
    y_lims: Tuple[numeric, numeric],
) -> Figure:
    fig: Figure = plot_guarantees(contract=contract, x_var=x_var, y_var=y_var, var_values=var_values, x_lims=x_lims, y_lims=y_lims)
    constraints: PolyhedralTermList = contract.a | contract.g
    fig.canvas.mpl_connect('button_press_event', lambda event: on_hover(constraints.evaluate(var_values).simplify(), x_var, y_var, fig, fig.axes[0], event))
    return fig
