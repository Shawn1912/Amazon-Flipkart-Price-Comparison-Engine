import tkinter as tk
from tkinter import font as tkfont


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
        for F in (EntryScreen, StartPage, PageOne, PageTwo):
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

        prod_name_label = tk.Label(
            self, text="Enter Product Name : ", font=controller.title_font
        )
        prod_name_label.pack()

        prod_name_entry = tk.Entry(self, width=20)
        prod_name_entry.pack()

        submit_button = tk.Button(
            self, text="Check prices", width=12, height=2, command=self.__submit()
        )
        submit_button.pack()

    def __submit(self):
        pass


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
