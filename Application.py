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
        print data

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

            print "{}: {}".format(wave, t_wave[wave])
            pass

        print t0

        t = np.arange(0, t0, 0.1)

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

            t_rel = ti - t_start

            A = data[wave]["A"]
            mu = data[wave]["mu"]
            b1 = data[wave]["b1"]
            b2 = data[wave]["b2"]

            if t_rel <= mu:
                b = b1
            else:
                b = b2

            return A * math.exp(-(t_rel-mu)**2/(2*b))
            pass

        y = [func(ti) for ti in t]

        plt.plot(t, y)
        plt.show()
        pass
    pass