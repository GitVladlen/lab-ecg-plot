import tkinter
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import numpy as np

# init data
holder = {
    "data": {
        "P": {
            "A": 0.15,
            "b1": 0.04,
            "b2": 0.04,
            "mu": 0.4
        },
        "Q": {
            "A": -0.14,
            "b1": 0.04,
            "b2": 0.04,
            "mu": 0.47
        },
        "R": {
            "A": 1.0,
            "b1": 0.03,
            "b2": 0.03,
            "mu": 0.5
        },
        "S": {
            "A": -0.24,
            "b1": 0.03,
            "b2": 0.03,
            "mu": 0.53
        },
        "ST": {
            "A": 0.0,
            "b1": 0.01,
            "b2": 0.01,
            "mu": 0.6
        },
        "T": {
            "A": 0.26,
            "b1": 0.05,
            "b2": 0.05,
            "mu": 0.7
        },
        "Alter": 1.0,
        "Noise": 1.0
    }
}


tooth_keys = ["P", "Q", "R", "S", "ST", "T"]
param_keys = ["A", "mu", "b1", "b2"]

# ecg model func
def fi(t, alter=False):
    result = 0

    Alter = holder["data"]["Alter"]
    Noise = holder["data"]["Noise"]

    for tooth_key in tooth_keys:
        A = holder["data"][tooth_key]["A"]
        mu = holder["data"][tooth_key]["mu"]

        b1 = holder["data"][tooth_key]["b1"]
        b2 = holder["data"][tooth_key]["b2"]

        if tooth_key == "T" and alter is  True:
            A = A + Alter

        b = np.where(t <= mu, b1, b2)

        noise = np.array([random.random() * Noise for _ in range(len(t))])

        result += A * np.exp(-(((t - mu) ** 2) / (2 * b ** 2))) + noise

    return result


# F = 60.0
# t0 = (60.0 * 1000.0) / F

t = np.arange(0.0, 1.0, 0.005)

# init gui
root = tkinter.Tk()
root.wm_title("Модель кардиоцикла")

# define options for opening or saving a file
file_open_opt = dict(
    defaultextension='.json',
    filetypes=[('json files', '.json'), ('all files', '.*')],
    initialdir='.\\',
    initialfile='ecg_data.json',
    parent=root,
    title='Open file'
)

file_save_opt = dict(
    defaultextension='.json',
    filetypes=[('json files', '.json'), ('all files', '.*')],
    initialdir='.\\',
    initialfile='ecg_data.json',
    parent=root,
    title='Save as file'
)


def on_load(file_name=None, update=True):
    try:
        if file_name is None:
            file_name = filedialog.askopenfilename(**file_open_opt)
        if file_name is None:
            return

        with open(file_name) as json_data:
            load_data = json.load(json_data)
            for tooth_key in tooth_keys:
                for param_key in param_keys:
                    holder["data"][tooth_key][param_key] = load_data[tooth_key][param_key]

            holder["data"]["Alter"] = load_data["Alter"]
            holder["data"]["Noise"] = load_data["Noise"]
            print(("on_load filename={}:\n{}".format(file_name, holder["data"])))
            pass
        pass
    except Exception as exception:
        print("Exception {}: {}".format(type(exception), exception))
        return
        pass
    if update:
        ecg_plot.set_ydata(fi(t))
        canvas.draw()
    pass

def on_save(file_name=None):
    try:
        if file_name is None:
            file_name = filedialog.asksaveasfilename(**file_save_opt)
        if file_name is None:
            return

        print("on_save filename={}:\n{}".format(file_name, holder["data"]))

        with open(file_name, 'w') as outfile:
            json.dump(holder["data"], outfile, indent=4, sort_keys=True)
            pass
        pass
    except Exception as exception:
        print("Exception {}: {}".format(type(exception), exception))
        return
        pass
    pass

on_load("ecg_data.json", False)

fig = Figure(figsize=(5, 4), dpi=100)

sub_plot = fig.add_subplot(111)

ecg_plot, = sub_plot.plot(t, fi(t), 'b')

sub_plot.set_ylabel('Напряжение (мВ)')
sub_plot.set_xlabel('Время (с)')
sub_plot.set_ylim([-0.5, 1.5])

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)

# vars
start_tooth_key = "T"

tooth = tkinter.StringVar()
tooth.set(start_tooth_key)

param_vars = {}

F_var = tkinter.StringVar()
F_var.set("60")

controll_pane = tkinter.PanedWindow(root)
controll_pane.pack(side=tkinter.RIGHT)

show_alter_var = tkinter.IntVar()
show_alter_var.set(0)

def choose_tooth(*args):
    tooth_key = tooth.get()
    tooth_data = holder["data"][tooth_key]

    for param_key in param_keys:
        new_value = tooth_data[param_key]

        param_vars[param_key].set(new_value)


def on_update_var(*args):
    tooth_key = tooth.get()
    tooth_data = holder["data"][tooth_key]

    for param_key in param_keys:
        tooth_data[param_key] = param_vars[param_key].get()

    holder["data"]["Alter"] = param_vars["Alter"].get()
    holder["data"]["Noise"] = param_vars["Noise"].get()

    ecg_plot.set_xdata(t)
    ecg_plot.set_ydata(fi(t, show_alter_var.get() == 1))
    canvas.draw()
    pass


label_frame_params = tkinter.LabelFrame(controll_pane, text="Параметры модели")
label_frame_params.pack(padx=5)

scale_pane = tkinter.PanedWindow(label_frame_params)
scale_pane.pack(side=tkinter.LEFT)

param_names = ["Амплитуда", "Время", "Левая граница", "Правая граница"]

for param_key, param_name in zip(param_keys, param_names):
    param_var = tkinter.DoubleVar()

    label_frame_scale = tkinter.LabelFrame(scale_pane, text=param_name)
    label_frame_scale.pack(padx=5, pady=5)

    tkinter.Scale(label_frame_scale,
                  from_=-1.0,
                  to=1.0,
                  orient=tkinter.HORIZONTAL,
                  length=400,
                  showvalue=1,
                  tickinterval=0.5,
                  resolution=0.005,
                  command=on_update_var,
                  variable=param_var).pack()

    value = holder["data"][start_tooth_key][param_key]

    param_var.set(value)

    param_vars[param_key] = param_var

label_frame_tooth = tkinter.LabelFrame(label_frame_params, text="Зубец")
label_frame_tooth.pack(padx=5, pady=5, fill=tkinter.BOTH, side=tkinter.RIGHT)

for val in tooth_keys:
    tkinter.Radiobutton(label_frame_tooth,
                        text=val,
                        variable=tooth,
                        padx=5,
                        command=choose_tooth,
                        value=val).pack()

label_frame_f = tkinter.LabelFrame(controll_pane, text="Чсс, уд./мин")
label_frame_f.pack(fill="both", expand="yes", padx=5, pady=5)

tkinter.Label(label_frame_f,
              text="F = ").pack(side=tkinter.LEFT, padx=5, pady=5)

tkinter.Button(label_frame_f,
               text="<").pack(side=tkinter.LEFT, padx=5, pady=5)

f_ent = tkinter.Entry(label_frame_f,
                      width=5,
                      justify=tkinter.LEFT,
                      textvariable=F_var).pack(side=tkinter.LEFT)

tkinter.Button(label_frame_f,
               text=">").pack(side=tkinter.LEFT, padx=5, pady=5)

tkinter.Button(label_frame_f,
               text="Сохранить",
               command=on_save).pack(side=tkinter.RIGHT, padx=5, pady=5)

tkinter.Button(label_frame_f,
               text="Открыть",
               command=on_load).pack(side=tkinter.RIGHT, padx=5, pady=5)

########################################
label_frame_gen = tkinter.LabelFrame(controll_pane, text="Генерация")
label_frame_gen.pack(fill="both", expand="yes", padx=5, pady=5)

gen_top_pane = tkinter.PanedWindow(label_frame_gen)
gen_top_pane.pack(side=tkinter.TOP)

cycles_var = tkinter.StringVar()
cycles_var.set("30")


def on_generate():
    plt.close()

    cycles = int(cycles_var.get())
    for cycle in range(cycles):
        plt.plot(t + cycle, fi(t, cycle % 2 == 0), "b-", label='linear')
        axes = plt.gca()
        axes.set_ylim([-0.5, 1.5])

    plt.title("Сгенерированная ЭКГ")
    plt.show()


def on_cycle_down():
    cycles = int(cycles_var.get())
    cycles = cycles - 1 if cycles - 1 >= 1 else 1
    cycles_var.set(str(cycles))


def on_cycle_up():
    cycles = int(cycles_var.get())
    cycles = cycles + 1 if cycles + 1 <= 100 else 100
    cycles_var.set(str(cycles))


tkinter.Label(gen_top_pane,
              text="К-во циклов:").pack(side=tkinter.LEFT, padx=5, pady=5)

tkinter.Button(gen_top_pane,
               text="<",
               command=on_cycle_down).pack(side=tkinter.LEFT, padx=5, pady=5)

cycle_ent = tkinter.Entry(gen_top_pane,
                          width=5,
                          justify=tkinter.LEFT,
                          textvariable=cycles_var).pack(side=tkinter.LEFT)

tkinter.Button(gen_top_pane,
               text=">",
               command=on_cycle_up).pack(side=tkinter.LEFT, padx=5, pady=5)

tkinter.Button(gen_top_pane,
               text="Генерация",
               command=on_generate).pack(side=tkinter.RIGHT, padx=5, pady=5)

tkinter.Checkbutton(gen_top_pane,
                    text="Показать альтернацию Т",
                    variable=show_alter_var,
                    command=on_update_var).pack(side=tkinter.RIGHT, padx=5, pady=5)

gen_middle_pane = tkinter.PanedWindow(label_frame_gen)
gen_middle_pane.pack(side=tkinter.TOP)

alt_r_var = tkinter.DoubleVar()

alt_r_frame_scale = tkinter.LabelFrame(gen_middle_pane,
                                       text="Уровень альтернации Т")
alt_r_frame_scale.pack(side=tkinter.LEFT, padx=5, pady=5)

tkinter.Scale(alt_r_frame_scale,
              from_=0.0,
              to=1.0,
              orient=tkinter.HORIZONTAL,
              length=220,
              showvalue=1,
              tickinterval=0.5,
              resolution=0.005,
              command=on_update_var,
              variable=alt_r_var).pack()

alt_r_value = holder["data"]["Alter"]
alt_r_var.set(alt_r_value)

param_vars["Alter"] = alt_r_var

########################################

noise_level_var = tkinter.DoubleVar()

noise_level_frame_scale = tkinter.LabelFrame(gen_middle_pane,
                                             text="Уровень шума")
noise_level_frame_scale.pack(side=tkinter.RIGHT, padx=5, pady=5)

tkinter.Scale(noise_level_frame_scale,
              from_=0.0,
              to=1.0,
              orient=tkinter.HORIZONTAL,
              length=220,
              showvalue=1,
              tickinterval=0.5,
              resolution=0.005,
              command=on_update_var,
              variable=noise_level_var).pack()

noise_level_value = holder["data"]["Noise"]
noise_level_var.set(noise_level_value)

param_vars["Noise"] = noise_level_var

tkinter.mainloop()
