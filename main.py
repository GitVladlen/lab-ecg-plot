from Tkinter import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    root = Tk()

    F = 70
    t0 = (60 * 1000) / F
    A = 5
    mu = 3
    b = 3

    x1 = np.arange(0, 7, 0.1)
    y1 = A * np.exp(-(x1-mu)**2/(2*b))

    x2 = np.arange(7, 14, 0.1)
    y2 = A * np.exp(-(x2-mu)**2/(2*b))    

    x = x1 + x2
    y = y1 + y2

    x = np.arange(0, 7, 0.1)
    y = A * np.exp(-(x-mu)**2/(2*b))
    lbl = Label(root, text="F")
    lbl.pack()

    ent = Entry(root)
    ent.pack()
    
    btn = Button(root, text="Button")
    def onClick(event):
        plt.plot(x, y)
        plt.show()
        pass
    btn.bind("<Button-1>", onClick)
    btn.pack()

    root.mainloop()
    pass

if __name__ == "__main__":
    main()
    pass