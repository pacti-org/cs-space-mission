from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from typing import List, Tuple


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
