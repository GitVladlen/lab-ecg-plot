from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
import math
import random

from SimpleTableInput import SimpleTableInput

import json


class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.rows = ["P", "Q", "R", "S", "ST", "T"]
        self.cols = ["A", "mu", "b1", "b2"]

        self.table = SimpleTableInput(self, self.rows, self.cols)
        self.table.pack(side="top", padx=3, pady=3, fill=X, expand=True)

        for child in self.table.winfo_children():
            child.grid_configure(padx=2, pady=2)
            pass

        control_frame = Frame(parent, padding="3 3 3 3")
        control_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        openfile = Button(control_frame, text="Open", command=self.on_load)
        openfile.bind("<Return>", lambda event: self.on_load())
        openfile.grid(row=0)
        openfile.focus_set()

        savefile = Button(control_frame, text="Save", command=self.on_save)
        savefile.bind("<Return>", lambda event: self.on_save())
        savefile.grid(row=0, column=1)
        """ var F controls """
        label = Label(control_frame, text="F:")
        label.grid(row=0, column=2)

        self.var_f = StringVar()
        self.var_f.set(60)

        ent = Entry(control_frame, textvariable=self.var_f, width=4)
        ent.grid(row=0, column=3)
        """ var A controls """
        label = Label(control_frame, text="Noise [%]:")
        label.grid(row=0, column=4)

        self.var_A = StringVar()
        self.var_A.set(10)

        ent = Entry(control_frame, textvariable=self.var_A, width=4)
        ent.grid(row=0, column=5)
        """ var T controls """
        label = Label(control_frame, text="Alternation [%]:")
        label.grid(row=0, column=6)

        self.var_T = StringVar()
        self.var_T.set(10)

        ent = Entry(control_frame, textvariable=self.var_T, width=4)
        ent.grid(row=0, column=7)

        submit = Button(control_frame, text="Plot ECG", command=self.on_submit)
        submit.bind("<Return>", lambda event: self.on_submit())
        submit.grid(row=0, column=8)

        for child in control_frame.winfo_children():
            child.grid_configure(padx=3, pady=3)
            pass

        # define options for opening or saving a file
        self.file_open_opt = dict(
            defaultextension = '.json',
            filetypes = [('json files', '.json'), ('all files', '.*')],
            initialdir = '.\\',
            initialfile = 'data.json',
            parent = parent,
            title= 'Open file'
            )

        self.file_save_opt = dict(
            defaultextension = '.json',
            filetypes = [('json files', '.json'), ('all files', '.*')],
            initialdir = '.\\',
            initialfile = 'data.json',
            parent = parent,
            title= 'Save as file'
            )
        
        pass

    def on_load(self, file_name=None):
        try:
            if file_name is None:
                file_name = filedialog.askopenfilename(**self.file_open_opt)
            if file_name is None:
                return

            with open(file_name) as json_data:
                data = json.load(json_data)
                print ("on_load filename={}:\n{}".format(file_name, data))

                for i_col, col in enumerate(self.cols):
                    for i_row, row in enumerate(self.rows):
                        self.table.set(i_row, i_col, data[row][col])
                        pass
                    pass
                pass
            pass
        except Exception as exception:
            print ("Exception {}: {}".format(type(exception), exception))
            return
            pass
        pass

    def on_save(self, file_name=None):
        try:
            if file_name is None:
                file_name = filedialog.asksaveasfilename(**self.file_save_opt)
            if file_name is None:
                return

            data = self.getDataDict()
            print ("on_save filename={}:\n{}".format(file_name, data))

            with open(file_name, 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
                pass
            pass
        except Exception as exception:
            print ("Exception {}: {}".format(type(exception), exception))
            return
            pass
        pass

    def getDataDict(self):
        table_data = self.table.get()
        return dict(zip(self.rows, [dict(zip(self.cols, row)) for row in table_data]))
        pass

    def on_submit(self):
        F = int(self.var_f.get())
        A = int(self.var_A.get())
        T = int(self.var_T.get())

        self.plot_ecg(F, A, T, 10)
        pass

    def on_close(self):
        plt.close()
        pass

    def plot_ecg(self, F, A_range_T_wave, mu_range_T_wave, cycles):
        plt.close()

        data = self.getDataDict()

        coef = (60 * 1000) / F

        A_range_R_wave = 10

        def func(ti, R_wave_A_coef, T_wave_A_coef, T_wave_mu_coef):
            sum = 0

            for wave in self.rows:
                A = data[wave]["A"] * coef
                mu = data[wave]["mu"] * coef
                b = data[wave]["b1" if ti <= mu else "b2"] * coef

                if wave == "R":
                    A += A * R_wave_A_coef
                elif wave == "T":
                    A += A * T_wave_A_coef
                    mu += mu * T_wave_mu_coef

                numerator = (ti-mu)**2
                denominator = -2 * b**2
                sum += A * math.exp(numerator/denominator)
            return sum

        t = np.arange(0, coef, 1)

        for cycle in range(cycles):
            R_wave_A_coef = random.randint(-A_range_R_wave, A_range_R_wave) / 100.0
            T_wave_A_coef = random.randint(-A_range_T_wave, A_range_T_wave) / 100.0
            T_wave_mu_coef = random.randint(-mu_range_T_wave, mu_range_T_wave) / 100.0

            y = [func(ti, R_wave_A_coef, T_wave_A_coef, T_wave_mu_coef) for ti in t]
            x = [ti + cycle * coef for ti in t]

            plt.plot(x, y, 'b-')
            pass

        plt.title("ECG")
        plt.show()
        pass
    pass