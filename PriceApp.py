import tkinter as tk
from tkinter import font as tkfont
import requests
from bs4 import BeautifulSoup
import pandas as pd
import flip
import amz

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
            # print(page_name)

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

    def getFlipRequest(self):
        data = {"products": [], "prices": [], "ratings": []}

        url = "https://www.flipkart.com/search?q="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        products_class = "_31qSD5"

        # search_input = input("Enter product name : ").replace(" ", "+")
        print("Flipkart getting userInput...")
        global product
        search_input = product
        print("Flipkart Product is : ", search_input)

        link = url + search_input

        source = requests.get(link, headers=headers)
        content = source.text
        soup = BeautifulSoup(content, "lxml")

        for a in soup.findAll("a", href=True, attrs={"class": products_class}):
            try:
                name = a.find("div", attrs={"class": "_3wU53n"})
                data["products"].append(name.text[:60])

                try:
                    price = a.find("div", attrs={"class": "_1vC4OE _2rQ-NK"})
                    data["prices"].append(
                        int(price.text.replace("₹", "").replace(",", ""))
                    )
                except AttributeError:
                    data["prices"].append("Not available")

                try:
                    rating = a.find("div", attrs={"class": "hGSR34"})
                    data["ratings"].append(rating.text)
                except AttributeError:
                    data["ratings"].append("Not available")

            except AttributeError:
                continue

        df = pd.DataFrame(
            {
                "Product": data["products"],
                "Price": data["prices"],
                "Rating": data["ratings"],
            }
        )
        df.to_csv("flip.csv", index=False, encoding="utf-8")

    def getAmzRequest(self):
        data = {"products": [], "prices": [], "ratings": []}

        url = "https://www.amazon.in/s?k="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        products_class = "sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"

        # search_input = input("Enter product name : ").replace(" ", "+")
        print("Amazon getting userInput...")
        global product
        search_input = product
        print("Amazon Product is : ", search_input)

        link = url + search_input + "&ref=nb_sb_noss_2"

        source = requests.get(link, headers=headers)
        content = source.text
        soup = BeautifulSoup(content, "lxml")

        for a in soup.findAll("div", attrs={"class": products_class}):

            try:
                name = a.find(
                    "span", attrs={"class": "a-size-medium a-color-base a-text-normal"}
                )
                data["products"].append(name.text[:60])

                try:
                    price = a.find("span", attrs={"class": "a-price-whole"})
                    # or a-offscreen for price with rupee symbol
                    data["prices"].append(int(price.text.replace(",", "")))
                except AttributeError:
                    data["prices"].append("Not available")

                try:
                    rating = a.find("span", attrs={"class": "a-icon-alt"})
                    data["ratings"].append(rating.text[:3])
                except AttributeError:
                    data["ratings"].append("Not available")

            except AttributeError:
                continue

        df = pd.DataFrame(
            {
                "Product": data["products"],
                "Price": data["prices"],
                "Rating": data["ratings"],
            }
        )
        df.to_csv("amz.csv", index=False, encoding="utf-8")

    def __submit(self):
        global product
        product = self.userInput.get()

        self.getFlipRequest()
        self.getAmzRequest()

        self.controller.show_frame("SelectScreen")


class SelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        flipLabel = tk.Label(
            self, text="Select Flipkart : ", font=controller.title_font
        )
        flipLabel.pack()

        # colnames = ["Product", "Price", "Rating"]
        # data = pd.read_csv("flip.csv", names=colnames)

        # products = data.Product.tolist()
        # prices = data.Price.tolist()
        # ratings = data.Rating.tolist()

        # var = tk.StringVar(self)
        # var.set(products[0])

        # flipOptions = tk.OptionMenu(self, var, *products)
        # flipOptions.pack()

        amzLabel = tk.Label(self, text="Select Amazon : ", font=controller.title_font)
        amzLabel.pack()

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
