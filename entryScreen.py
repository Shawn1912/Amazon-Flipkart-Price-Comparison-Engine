from tkinter import *


class EntryScreen:
    master = None
    frame = None
    prod_name_label = None
    prod_name_entry = None
    submit_button = None

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, background="#b22222")
        self.frame.pack(fill=None, expand=False)

        self.prod_name_label = Label(self.frame, text="Enter Product Name : ")
        self.prod_name_label.pack()

        self.prod_name_entry = Entry(self.frame, width=20)
        self.prod_name_entry.pack()

        self.submit_button = Button(
            self.frame, text="Check prices", width=12, height=2, command=self.__submit
        )
        self.submit_button.pack()

    def __submit(self):
        import productComparison

        canvas = productComparison.create(self.master, self.emailID)


masterWin = {"width": 400, "height": 150, "xPos": 600, "yPos": 300}
master = Tk()
master.title("Price Comparison")
master.geometry(
    "{}x{}+{}+{}".format(
        masterWin["width"], masterWin["height"], masterWin["xPos"], masterWin["yPos"]
    )
)
master.config(bg="white")
screen = EntryScreen(master)
master.mainloop()
