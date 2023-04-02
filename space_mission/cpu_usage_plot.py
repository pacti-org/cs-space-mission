import psutil
import time
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from IPython.display import display, clear_output, update_display, Image
import ipywidgets as widgets
import threading
from contextlib import contextmanager
from io import BytesIO

# Function to get the current CPU usage percentage
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

@contextmanager
def cpu_usage_plot():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_ylim(0, 101)
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Usage (%)")

    cpu_usage_data = []
    max_data_points = 50
    line, = ax.plot(cpu_usage_data)

    plot_output = widgets.Output()
    display(plot_output)

    def update_plot():
        nonlocal cpu_usage_data
        cpu_usage = get_cpu_usage()
        cpu_usage_data.append(cpu_usage)

        if len(cpu_usage_data) > max_data_points:
            cpu_usage_data.pop(0)

        line.set_ydata(cpu_usage_data)
        line.set_xdata(range(len(cpu_usage_data)))

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img = Image(data=buf.read())

        with plot_output:
            clear_output(wait=True)
            display(img)

        ax.relim()
        ax.autoscale_view()

    def stop_condition():
        nonlocal stop
        return stop

    def display_cpu_usage_plot_widget(stop_condition):
        nonlocal stop
        try:
            while not stop_condition():
                update_plot()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass

    stop = False
    cpu_usage_plot_thread = threading.Thread(target=display_cpu_usage_plot_widget, args=(stop_condition,), daemon=True)
    cpu_usage_plot_thread.start()

    try:
        yield
    finally:
        stop = True
        cpu_usage_plot_thread.join()
        with plot_output:
            clear_output(wait=True)
