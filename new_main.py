import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

data = []
with open('ЕКГ_КП5.txt', 'r') as reader:
    for line in reader:
        line_data = map(lambda x: float(x), filter(lambda x: x != '' and x != '\n', line.split(" ")))
        data += line_data


def calc_alpha_data(alpha_, data_):
    new_data_ = []
    for k in range(len(data_)):
        z_tilda_prev = 0
        if k-1 >= 0:
            z_tilda_prev = new_data_[k-1]
        z_tilda = z_tilda_prev + alpha_*(data_[k] - z_tilda_prev)

        new_data_.append(z_tilda)
    return new_data_


def calc_window_data(window_, data_):
    if window_ == 0:
        return data_
    new_data_ = []
    lamb = 1 / window_
    for k in range(len(data_)):
        z_prev = 0
        if k-1 >= 0:
            z_prev = new_data_[k-1]
        z_window = 0
        if k-window_ >= 0:
            z_window = data_[k - window_]

        z = z_prev + lamb*(data_[k]-z_window)

        new_data_.append(z)
    return new_data_


def calc_window_data_2(window_, data_):
    if window_ == 0:
        return data_
    new_data_ = []
    mu = 1 / (1+2*window_)
    for k in range(len(data_)):
        z_tilda_prev = 0
        if k-1 >= 0:
            z_tilda_prev = new_data_[k-1]
        z_next = 0
        if k+window_ < len(data_):
            z_next = data_[k+window_]
        z_prev = 0
        if k-1-window_ >= 0:
            z_prev = data_[k-1-window_]

        z_tilda = z_tilda_prev + mu*(z_next-z_prev)

        new_data_.append(z_tilda)
    return new_data_


def calc_adaptive_window_data(window_, h_, data_):
    if window_ == 0:
        return data_
    new_data_ = []
    Wk = window_
    for k in range(len(data_)):
        z_tilda = 0
        for Wk_i in reversed(range(1, window_+1)):
            if abs(Wk_i - Wk) <= 1:
                mu = 1 / (2 * Wk_i + 1)
                summa = 0
                for j in range(-Wk_i, Wk_i+1):
                    z_k_minus_j = 0
                    if 0 <= k-j < len(data_):
                        z_k_minus_j = data_[k-j]
                    summa += z_k_minus_j
                z_tilda_i = mu * summa
                if abs(z_tilda_i-data_[k]) <= h_:
                    z_tilda = z_tilda_i
                    Wk = Wk_i
                    break
        if z_tilda == 0:
            z_tilda = data[k]
        new_data_.append(z_tilda)
    return new_data_


alpha = 0.7
w0 = 10

root = tkinter.Tk()
root.wm_title("Сглаживание ЕКГ")

fig = Figure(figsize=(14, 3), dpi=100)

sub_plot = fig.add_subplot(111)

ecg_plot, = sub_plot.plot(data)

sub_plot.set_ylabel('Напряжение (мВ)')
sub_plot.set_xlabel('Номер точки k')
sub_plot.set_ylim([-1, 1.5])

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

var_mode = tkinter.IntVar()
var_mode.set(1)

param_alpha_enable_var = tkinter.IntVar()
param_alpha_window_var = tkinter.IntVar()

param_alpha_enable_var.set(1)
param_alpha_window_var.set(0)

param_alpha_var = tkinter.DoubleVar()
param_alpha_var.set(alpha)

param_window_var = tkinter.IntVar()
param_window_var.set(w0)

param_h_var = tkinter.DoubleVar()
param_h_var.set(0.5)


def update_plot(*args):
    mode = var_mode.get()
    if mode == 1:
        ecg_plot.set_ydata(data)
    elif mode == 2:
        updated_alpha = param_alpha_var.get()
        updated_data = calc_alpha_data(updated_alpha, data)
        ecg_plot.set_ydata(updated_data)
    elif mode == 3:
        updated_window = param_window_var.get()
        updated_data = calc_window_data(updated_window, data)
        ecg_plot.set_ydata(updated_data)
    elif mode == 4:
        updated_window = param_window_var.get()
        updated_data = calc_window_data_2(updated_window, data)
        ecg_plot.set_ydata(updated_data)
    elif mode == 5:
        updated_window = param_window_var.get()
        updated_h = param_h_var.get()
        updated_data = calc_adaptive_window_data(updated_window, updated_h, data)
        ecg_plot.set_ydata(updated_data)

    canvas.draw()
    pass


controll_pane = tkinter.PanedWindow(root)
controll_pane.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)

label_frame_params = tkinter.LabelFrame(controll_pane, text="Параметры сглаживания")
label_frame_params.pack(pady=5, padx=5, fill=tkinter.BOTH, expand=1)

scale_pane = tkinter.PanedWindow(label_frame_params)
scale_pane.pack(side=tkinter.LEFT)

tkinter.Scale(scale_pane,
              label="Параметр альфа (alpha)",
              from_=0.0,
              to=1.0,
              orient=tkinter.HORIZONTAL,
              length=300,
              showvalue=1,
              tickinterval=0.2,
              resolution=0.05,
              command=update_plot,
              variable=param_alpha_var).pack()

tkinter.Scale(scale_pane,
              label="Ширина окна (W0)",
              from_=0,
              to=50,
              orient=tkinter.HORIZONTAL,
              length=300,
              showvalue=1,
              tickinterval=5,
              command=update_plot,
              variable=param_window_var).pack()

tkinter.Scale(scale_pane,
              label="Порог переглаживания (h0)",
              from_=0.0,
              to=1.0,
              orient=tkinter.HORIZONTAL,
              length=300,
              tickinterval=0.2,
              resolution=0.005,
              command=update_plot,
              variable=param_h_var).pack()

tkinter.Radiobutton(label_frame_params,
                    text="Без сглаживания",
                    variable=var_mode,
                    value=1,
                    command=update_plot).pack(anchor=tkinter.W)

tkinter.Radiobutton(label_frame_params,
                    text="Экспоненциальное сглаживание:\n(z'[k]=z'[k-1]+alpha*(z[k]-z'[k-1])",
                    variable=var_mode,
                    value=2,
                    justify=tkinter.LEFT,
                    command=update_plot).pack(anchor=tkinter.W)

tkinter.Radiobutton(label_frame_params,
                    text="Скользящее среднее 1:\n(z'[k]=z'[k-1]+l(z[k]-z[k-W0])), l=1/W0",
                    variable=var_mode,
                    value=3,
                    justify=tkinter.LEFT,
                    command=update_plot).pack(anchor=tkinter.W)

tkinter.Radiobutton(label_frame_params,
                    text="Скользящее среднее 2:\n(z'[k]=z'[k-1]+mu(z[k+W0]-z[k-1-W0])), mu=1/(1+2*W0)",
                    variable=var_mode,
                    value=4,
                    justify=tkinter.LEFT,
                    command=update_plot).pack(anchor=tkinter.W)

tkinter.Radiobutton(label_frame_params,
                    text="Адаптивное сглаживание:\nz'[k]=1/(2*Wk+1) * sum[j=-Wk...Wk](z[k-j]), Wk<=W0, |z'[k]-z[k]<=h0|, |Wk-W0|<=1",
                    variable=var_mode,
                    value=5,
                    justify=tkinter.LEFT,
                    command=update_plot).pack(anchor=tkinter.W)

root.mainloop()