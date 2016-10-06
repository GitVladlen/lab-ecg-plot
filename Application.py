from Tkinter import *
from ttk import *

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
        self.table.pack(side="top", fill="both", expand=True)

        control_frame = Frame(parent, padding="3 3 3 3")
        control_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        label = Label(control_frame, text="File name (*.json):")
        label.grid(row=0)

        self.file_name = StringVar()

        ent = Entry(control_frame, textvariable=self.file_name)
        ent.grid(row=0, column=1)
        ent.focus_set()

        openfile = Button(control_frame, text="Open", command=self.on_load)
        openfile.grid(row=0, column=2)

        savefile = Button(control_frame, text="Save", command=self.on_save)
        savefile.grid(row=0, column=3)

        submit = Button(control_frame, text="Plot ECG", command=self.on_submit)
        submit.grid(row=0, column=4)

        for child in control_frame.winfo_children():
            child.grid_configure(padx=3, pady=3)
            pass

    def on_load(self, file_name=None):
        if file_name is None:
            file_name = self.file_name.get()
            if file_name == "":
                return
            pass
        try:
            with open(file_name) as json_data:
                data = json.load(json_data)
                print "on_load:", data
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

    def on_save(self):
        try:
            data = self.getDataDict()
            print "on_save:", data
            
            file_name = self.file_name.get()
            if file_name == "":
                file_name = "data.json"
                pass

            with open(self.file_name, 'w') as outfile:
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
        self.plot_ecg(70)
        pass

    def on_close(self):
        # self.on_save()
        plt.close()
        pass

    def plot_ecg(self, F):
        data = self.getDataDict()
        # print data

        # t0 = (60 * 1000) / F
        # print t0

        t0 = 0
        t_wave = {}
        for wave in self.rows:
            mu = data[wave]["mu"]
            b1 = data[wave]["b1"]
            b2 = data[wave]["b2"]

            t1i = mu - 3 * b1
            t2i = mu + 3 * b2
            t_wave[wave] = (t1i, t2i)

            t0 += t2i - t1i

            # print "{}: {}".format(wave, t_wave[wave])
            pass

        # print t0

        t = np.arange(-50, t0+50, 0.1)

        def get_wave(ti):
            prev_ti = 0
            for wave in self.rows:
                t1i, t2i = t_wave[wave]

                t1i += prev_ti
                t2i += prev_ti

                if t1i <= ti < t2i:
                    return wave, t1i
                    pass

                prev_ti = t2i
                pass

            return None, None
            pass

        def func(ti):
            wave, t_start = get_wave(ti)

            if wave is None:
                return 0
                pass

            t_rel = ti - t_start

            A = data[wave]["A"]
            mu = data[wave]["mu"]
            b1 = data[wave]["b1"]
            b2 = data[wave]["b2"]

            if t_rel <= mu:
                b = b1
            else:
                b = b2

            return A * math.exp(-((t_rel-mu)**2)/(2*b**2))
            pass

        y = [func(ti) for ti in t]
        ax = plt.axes()
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        plt.plot(t, y)
        plt.title("ECG")
        plt.show()
        pass
    pass