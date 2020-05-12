from tkinter import *


def create(master):
    row = 0
    master.geometry("800x600")
    canvas = Canvas(master)
    canvas.pack()
    master.mainloop()
    return canvas
