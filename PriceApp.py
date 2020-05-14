import tkinter as tk
from tkinter import font as tkfont
import pandas as pd
import flip

product = ""


class PriceApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Price Comparison Engine")
        masterWin = {"width": 400, "height": 150, "xPos": 600, "yPos": 300}
        self.geometry(
            "{}x{}+{}+{}".format(
                masterWin["width"],
                masterWin["height"],
                masterWin["xPos"],
                masterWin["yPos"],
            )
        )
        self.config(bg="white")

        self.title_font = tkfont.Font(
            family="Helvetica", size=18, weight="bold", slant="italic"
        )

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (EntryScreen, SelectScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            print(page_name)

        self.show_frame("EntryScreen")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class EntryScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        prodNameLabel = tk.Label(
            self, text="Enter Product Name : ", font=controller.title_font
        )
        prodNameLabel.pack()

        self.userInput = tk.StringVar()

        prodNameEntry = tk.Entry(self, width=20, textvariable=self.userInput)
        prodNameEntry.pack()
        prodNameEntry.focus()

        submitButton = tk.Button(
            self, text="Check prices", width=12, height=2, command=self.__submit,
        )
        # command=lambda: controller.show_frame("SelectScreen"),
        submitButton.pack()

    def __submit(self):
        global product
        print(product)
        product = self.userInput.get()
        print(product)
        flip.getRequest()
        self.controller.show_frame("SelectScreen")


class SelectScreen(tk.Frame,):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        flipSelect = tk.Label(
            self, text="Select Flipkart : ", font=controller.title_font
        )
        flipSelect.pack()

        # colnames = ["Product", "Price", "Rating"]
        # data = pd.read_csv("flip.csv", names=colnames)

        # products = data.Product.tolist()
        # prices = data.Price.tolist()
        # ratings = data.Rating.tolist()

        # var = tk.StringVar(self)
        # var.set(products[0])

        # flipOptions = tk.OptionMenu(self, var, *products)
        # flipOptions.pack()

        amzSelect = tk.Label(self, text="Select Amazon : ", font=controller.title_font)
        amzSelect.pack()

        # amzList = [1, 2, 3, 4, 5]
        # var = tk.StringVar(self)
        # var.set(amzList[0])

        # amzOptions = tk.OptionMenu(self, var, *amzList)
        # amzOptions.pack()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self, text="This is the start page", font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(
            self,
            text="Go to Page One",
            command=lambda: controller.show_frame("PageOne"),
        )
        button2 = tk.Button(
            self,
            text="Go to Page Two",
            command=lambda: controller.show_frame("PageTwo"),
        )
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(
            self,
            text="Go to the start page",
            command=lambda: controller.show_frame("StartPage"),
        )
        button.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(
            self,
            text="Go to the start page",
            command=lambda: controller.show_frame("StartPage"),
        )
        button.pack()


if __name__ == "__main__":
    app = PriceApp()
    app.mainloop()
