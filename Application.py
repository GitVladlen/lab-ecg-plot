from Tkinter import *
from ttk import *

import matplotlib.pyplot as plt
import numpy as np
import math

from SimpleTableInput import SimpleTableInput

import json


class Application(Frame):
    def __init__(self, parent, file_name='data.json'):
        Frame.__init__(self, parent)
        self.file_name = file_name
        self.rows = ["P", "Q", "R", "S", "ST", "T"]
        self.cols = ["A", "mu", "b1", "b2"]

        self.table = SimpleTableInput(self, self.rows, self.cols)
        self.submit = Button(self, text="Submit", command=self.on_submit)
        self.save = Button(self, text="Save", command=self.on_save)
        self.table.pack(side="top", fill="both", expand=True)
        self.submit.pack(side="bottom")
        self.save.pack(side="bottom")

    def on_load(self, file_name=None):
        if file_name is None:
            file_name = self.file_name
            pass
        try:
            with open(file_name) as json_data:
                data = json.load(json_data)
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
            table_data = self.table.get()
            data = dict(zip(self.rows, [dict(zip(self.cols, row)) for row in table_data]))
            print data

            with open(self.file_name, 'w') as outfile:
                json.dump(data, outfile, indent=4, sort_keys=True)
                pass
            pass
        except Exception as exception:
            print "Exception {}: {}".format(type(exception), exception)
            return
            pass
        pass

    def on_submit(self):
        self.plot_ecg(1, 1, 1, 1)
        pass

    def on_close(self):
        self.on_save()
        plt.close()
        pass

    def plot_ecg(self, F, A, mu, b):
        t0 = (60 * 1000) / F

        t_p = 7
        t_q = 7

        t0 = t_p + t_q

        x = np.arange(0, t0, 0.1)

        def func(x):
            if x < t_p:
                return A * math.exp(-(x-mu)**2/(2*b))
                pass

            return 1.5 * A * math.exp(-(x-t_p-5)**2/(2*b))
            pass

        y = [func(xx) for xx in x]

        plt.plot(x, y)
        plt.show()
        pass
    pass