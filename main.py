from Tkinter import *
from ttk import *

from Application import Application

def main():
    root = Tk()
    root.title("ECG Plot emulator")

    app = Application(root, 'data.json')
    app.on_load()
    app.pack(side=TOP, fill=BOTH, expand=True)

    def closeWindow(*args):
        app.on_close()
        root.destroy()
        pass

    def submit(*args):
        app.on_submit()
        pass

    root.bind("<Escape>", closeWindow)
    root.protocol("WM_DELETE_WINDOW", closeWindow)

    root.bind("<Return>", submit)

    root.mainloop()
    pass

if __name__ == "__main__":
    main()
    pass