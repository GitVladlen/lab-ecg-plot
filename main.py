from tkinter import *

from Application import Application

def main():
    root = Tk()
    root.title("ECG Plot")

    app = Application(root)
    app.on_load('data.json')
    app.pack(side=TOP, fill=BOTH, expand=True)

    def closeWindow(*args):
        app.on_close()
        root.destroy()
        pass

    root.bind("<Escape>", closeWindow)
    root.protocol("WM_DELETE_WINDOW", closeWindow)

    root.mainloop()
    pass

if __name__ == "__main__":
    main()
    pass