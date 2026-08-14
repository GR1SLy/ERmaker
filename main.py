import tkinter
import sys
import os
from lib.gui import App

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()