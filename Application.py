from Tkinter import *
from ttk import *
import tkFileDialog

import matplotlib.pyplot as plt
import numpy as np
import math

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

        label = Label(control_frame, text="F:")
        label.grid(row=0, column=2)

        self.var_f = StringVar()
        self.var_f.set(60)

        ent = Entry(control_frame, textvariable=self.var_f, width=4)
        ent.grid(row=0, column=3)

        submit = Button(control_frame, text="Plot ECG", command=self.on_submit)
        submit.bind("<Return>", lambda event: self.on_submit())
        submit.grid(row=0, column=4)

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
                file_name = tkFileDialog.askopenfilename(**self.file_open_opt)
            if file_name is None:
                return

            with open(file_name) as json_data:
                data = json.load(json_data)
                print "on_load filename={}:\n{}".format(file_name, data)

                for i_col, col in enumerate(self.cols):
                    for i_row, row in enumerate(self.rows):
                        self.table.set(i_row, i_col, data[row][col])
                        pass
                    pass
                pass
            pass
        except Exception as exception:
            print "Exception {}: {}".format(type(exception), exception)
            return
            pass
        pass

    def on_save(self, file_name=None):
        try:
            if file_name is None:
                file_name = tkFileDialog.asksaveasfilename(**self.file_save_opt)
            if file_name is None:
                return

            data = self.getDataDict()
            print "on_save filename={}:\n{}".format(file_name, data)

            with open(file_name, 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
                pass
            pass
        except Exception as exception:
            print "Exception {}: {}".format(type(exception), exception)
            return
            pass
        pass

    def getDataDict(self):
        table_data = self.table.get()
        return dict(zip(self.rows, [dict(zip(self.cols, row)) for row in table_data]))
        pass

    def on_submit(self):
        F = int(self.var_f.get())
        self.plot_ecg(F)
        pass

    def on_close(self):
        plt.close()
        pass

    def plot_ecg(self, F):
        plt.close()

        data = self.getDataDict()

        coef = (60 * 1000) / F

        def func(ti):
            sum = 0
            for wave in self.rows:
                A = data[wave]["A"] * coef
                mu = data[wave]["mu"] * coef
                b = data[wave]["b1" if ti <= mu else "b2"]  * coef

                numerator = (ti-mu)**2
                denominator = -2 * b**2
                sum += A * math.exp(numerator/denominator)
            return sum

        t = np.arange(0, coef, 1)
        y = [func(ti) for ti in t]

        plt.plot(t, y, "b-")

        plt.title("ECG")
        plt.show()
        pass
    pass