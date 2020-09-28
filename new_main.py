import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np

# init data
data = {
    "P": {
        "A": 0.2,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 0.6
    },
    "Q": {
        "A": -0.11,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 1.2
    },
    "R": {
        "A": 1.0,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 1.8
    },
    "S": {
        "A": -0.18,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 2.4
    },
    "ST": {
        "A": 0.0,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 3
    },
    "T": {
        "A": 0.28,
        "b1": 0.1,
        "b2": 0.1,
        "mu": 3.6
    }
}

tooth_keys = ["P", "Q", "R", "S", "ST", "T"]
param_keys = ["A", "mu", "b1", "b2"]


# ecg model func
def fi(t):
    result = 0
    for tooth_key in tooth_keys:
        A = data[tooth_key]["A"]
        mu = data[tooth_key]["mu"]

        b1 = data[tooth_key]["b1"]
        b2 = data[tooth_key]["b2"]

        b = np.where(t <= mu, b1, b2)

        result += A * np.exp(-(((t - mu) ** 2) / (2 * b ** 2)))
    return result


# F = 60.0
# t0 = (60.0 * 1000.0) / F

t = np.arange(-1.0, 5.0, 0.05)

# init gui
root = tkinter.Tk()
root.wm_title("ECG cycle model")

fig = Figure(figsize=(5, 4), dpi=100)

ecg_plot, = fig.add_subplot(111).plot(t, fi(t), 'b')

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

pane = tkinter.PanedWindow(root)
# vars
start_tooth_key = "T"

tooth = tkinter.StringVar()
tooth.set(start_tooth_key)

param_vars = {}


def choose_tooth(*args):
    tooth_key = tooth.get()
    tooth_data = data[tooth_key]

    for param_key in param_keys:
        new_value = tooth_data[param_key]

        param_vars[param_key].set(new_value)


def on_update_var(*args):
    tooth_key = tooth.get()
    tooth_data = data[tooth_key]

    for param_key in param_keys:
        tooth_data[param_key] = param_vars[param_key].get()

    ecg_plot.set_ydata(fi(t))
    canvas.draw()
    pass


tkinter.Label(pane,
              text="Choose tooth:",
              padx=15,
              justify=tkinter.LEFT).pack(side=tkinter.LEFT)

for val in tooth_keys:
    tkinter.Radiobutton(pane,
                        text=val,
                        variable=tooth,
                        padx=15,
                        command=choose_tooth,
                        value=val).pack(anchor=tkinter.W, side=tkinter.LEFT)

pane.pack()

for param_key in param_keys:
    param_var = tkinter.DoubleVar()

    scale_pane = tkinter.PanedWindow(root)

    tkinter.Label(scale_pane,
                  text="{}:".format(param_key),
                  padx=15,
                  justify=tkinter.LEFT).pack(side=tkinter.LEFT)

    tkinter.Scale(scale_pane,
                  from_=-1.0,
                  to=4.0,
                  orient=tkinter.HORIZONTAL,
                  length=500,
                  showvalue=1,
                  tickinterval=0.5,
                  resolution=0.01,
                  command=on_update_var,
                  variable=param_var).pack(side=tkinter.RIGHT)

    scale_pane.pack()

    value = data[start_tooth_key][param_key]

    param_var.set(value)

    param_vars[param_key] = param_var

tkinter.mainloop()
