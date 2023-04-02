import psutil
import time
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from IPython.display import display, clear_output, Image
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
    # the upper limit is 101 so that we can see data points with y=100
    ax.set_ylim(0, 101) 
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Usage (%)")

    cpu_usage_data = []
    max_data_points = 50
    line, = ax.plot(cpu_usage_data)
    fill = ax.fill_between(range(len(cpu_usage_data)), cpu_usage_data, 0, alpha=0.3)

    img = widgets.Image()
    display_handle = display(img, display_id=True)

    def update_plot():
        nonlocal cpu_usage_data
        cpu_usage = get_cpu_usage()
        cpu_usage_data.append(cpu_usage)

        if len(cpu_usage_data) > max_data_points:
            cpu_usage_data.pop(0)

        ax.clear()
        # bump the limit by one to see data with y=100
        ax.set_ylim(0, 101)
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU Usage (%)")
        
        line, = ax.plot(range(len(cpu_usage_data)), cpu_usage_data)
        ax.fill_between(range(len(cpu_usage_data)), cpu_usage_data, 0, alpha=0.3)

        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img.value = buf.read()

        display_handle.update(img)

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
        clear_output(wait=True)

    # Display the final plot as part of the notebook
    matplotlib.use('module://ipykernel.pylab.backend_inline')
    fig.savefig(BytesIO(), format='png')  # This line is necessary to refresh the plot for the inline backend
    plt.show()
