import tkinter as tk
from tkinter import font as tkfont
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd

product = ""
# flipData = {"products": [], "prices": [], "ratings": []}
# amzData = {"products": ["sample"], "prices": [], "ratings": []}
flipData = {}
amzData = {}


class PriceApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Price Comparison Engine")
        masterWin = {"width": 1000, "height": 700, "xPos": 250, "yPos": 50}
        self.geometry(
            "{}x{}+{}+{}".format(
                masterWin["width"],
                masterWin["height"],
                masterWin["xPos"],
                masterWin["yPos"],
            )
        )
        self.config(bg="white")

        # Bold fonts
        self.titleFont = tkfont.Font(family="Helvetica", size=30, weight="bold")
        self.largeBoldFont = tkfont.Font(family="Helvetica", size=15, weight="bold")
        self.mediumBoldFont = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.smallBoldFont = tkfont.Font(family="Helvetica", size=10, weight="bold")

        # Normal fonts
        self.largeFont = tkfont.Font(family="Helvetica", size=15)
        self.mediumFont = tkfont.Font(family="Helvetica", size=12)
        self.smallFont = tkfont.Font(family="Helvetica", size=10)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg="black")
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

        # frame = tk.Frame(
        #     self,
        #     bg="black",
        #     height=300,
        #     width=600,
        #     bd=1,
        #     relief=tk.SUNKEN,
        #     borderwidth=5,
        # )
        # # frame.pack(fill=tk.X, padx=5, pady=5)
        # frame.place(x=200, y=200)

        frame = tk.Frame(
            self,
            bg="black",
            height=700,
            width=1000,
            bd=1,
            relief=tk.SUNKEN,
            borderwidth=5,
        )
        # frame.pack(fill=tk.X, padx=5, pady=5)
        frame.place(x=0, y=0)

        prodNameLabel = tk.Label(
            frame,
            text="Enter Product Name : ",
            font=controller.largeBoldFont,
            bg="black",
            fg="white",
        )
        prodNameLabel.place(x=100, y=100)

        self.userInput = tk.StringVar()

        prodNameEntry = tk.Entry(frame, width=20, textvariable=self.userInput)
        prodNameEntry.place(x=340, y=105)
        prodNameEntry.focus()

        submitButton = tk.Button(
            frame,
            text="Check prices",
            width=12,
            height=2,
            bg="green",
            fg="white",
            command=self.__submit,
        )
        # command=lambda: controller.show_frame("SelectScreen"),
        # submitButton.place(x=230, y=200)   CENTER POSITION
        submitButton.place(x=110, y=200)

        cancelButton = tk.Button(
            frame, text="Exit", width=12, height=2, bg="red", fg="white"
        )
        # command=lambda: controller.show_frame("SelectScreen"),
        cancelButton.place(x=360, y=200)
        """ 
        #0099ff blue
        #ffcc00 yellow
        #ff0000 red
        """

    def __getFlipRequest(self):
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
                    data["prices"].append("N.A")

                try:
                    rating = a.find("div", attrs={"class": "hGSR34"})
                    data["ratings"].append(rating.text)
                except AttributeError:
                    data["ratings"].append("N.A")

            except AttributeError:
                continue

        df = pd.DataFrame(
            {
                "Select Product": data["products"],
                "Price": data["prices"],
                "Rating": data["ratings"],
            }
        )
        df.to_csv("flip.csv", index=False, encoding="utf-8")
        return data

    def __getAmzRequest(self):
        data = {"products": [], "prices": [], "ratings": []}

        url = "https://www.amazon.in/s?k="
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        products_class_rows = "sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"
        products_class_boxes = "sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"

        # search_input = input("Enter product name : ").replace(" ", "+")
        print("Amazon getting userInput...")
        global product
        search_input = product
        print("Amazon Product is : ", search_input)

        link = url + search_input + "&ref=nb_sb_noss_2"

        source = requests.get(link, headers=headers)
        content = source.text
        soup = BeautifulSoup(content, "lxml")

        products = soup.findAll("div", attrs={"class": products_class_rows})

        # for i in range(1, len(products) // 4):
        #     print(products[i])
        # print(len(products))
        # print(type(products))

        # print(products[1])

        if len(products) != 1:
            for prod in products:
                try:
                    name = prod.find(
                        "span",
                        attrs={"class": "a-size-medium a-color-base a-text-normal"},
                    )
                    data["products"].append(name.text[:60])

                    try:
                        price = prod.find("span", attrs={"class": "a-price-whole"})
                        data["prices"].append(int(price.text.replace(",", "")))
                    except AttributeError:
                        data["prices"].append("N.A")

                    try:
                        rating = prod.find("span", attrs={"class": "a-icon-alt"})
                        data["ratings"].append(rating.text[:3])
                    except AttributeError:
                        data["ratings"].append("N.A")

                except AttributeError:
                    continue
        else:
            # products not in row form
            # add for loop for scraping product boxes
            data["products"].append("No products available")
            data["prices"].append("NA")
            data["ratings"].append("NA")

        df = pd.DataFrame(
            {
                "Select Product": data["products"],
                "Price": data["prices"],
                "Rating": data["ratings"],
            }
        )
        df.to_csv("amz.csv", index=False, encoding="utf-8")

        return data

    def __submit(self):
        global product, flipData, amzData
        product = self.userInput.get()

        flipData = self.__getFlipRequest()
        # print(flipData["products"])
        amzData = self.__getAmzRequest()
        # print(amzData["products"])

        # SelectScreen.__showOptions(self=SelectScreen)
        self.controller.show_frame("SelectScreen")


class SelectScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        """ FLIPKART AREA """
        # Flipkart Frame
        flip = tk.Frame(
            self,
            bg="#ffffb3",
            height=300,
            width=400,
            bd=1,
            relief=tk.SUNKEN,
            borderwidth=5,
        )
        # flip.pack(fill=tk.X, padx=5, pady=5)
        flip.place(x=10, y=10)

        # Flipkart product label
        flipProductLabel = tk.Label(
            flip, text="Product : ", font=controller.mediumBoldFont
        )
        flipProductLabel.place(x=10, y=20)

        # Reading the saved CSV file
        flipColnames = ["Product", "Price", "Rating"]
        flipData = pd.read_csv("flip.csv", names=flipColnames)

        # Assigning columns from CSV to variables
        flipProducts = flipData.Product.tolist()
        flipPrices = flipData.Price.tolist()
        flipRatings = flipData.Rating.tolist()

        # Variable which points to the selected option in dropdown menu
        flipOptionVar = tk.StringVar(flip)
        # Setting the first element of flipProducts as selected option
        flipOptionVar.set(flipProducts[0])

        # Products dropdown menu
        """ tk.OptionMenu(master, variable, values) """
        flipOptions = tk.OptionMenu(flip, flipOptionVar, *flipProducts)
        flipOptions.place(x=120, y=17)

        # Price label
        flipPriceLabel = tk.Label(flip, text="Price : ", font=controller.smallBoldFont)
        flipPriceLabel.place(x=10, y=60)

        # Rating Label
        flipRatingLabel = tk.Label(
            flip, text="Rating : ", font=controller.smallBoldFont
        )
        flipRatingLabel.place(x=150, y=60)

        # TODO: Test price and rating fetch
        def onFlipOptionSelected():
            # Getting the product selected and its index in the products list
            selectedProduct = flipOptionVar.get()
            indexOfSelectedProduct = flipProducts.index(selectedProduct)

            # Getting price from the prices list and setting the label text
            priceOfSelectedProduct = str(flipPrices[indexOfSelectedProduct])
            flipPriceLabel.config(text="Price : " + priceOfSelectedProduct)

            # Getting rating from the ratings list and setting the label text
            ratingOfSelectedProduct = flipRatings[indexOfSelectedProduct]
            flipRatingLabel.config(text="Rating : " + ratingOfSelectedProduct)

        # Visit page button
        visitFlipButton = tk.Button(
            flip, text="Check price and rating", command=onFlipOptionSelected
        )
        visitFlipButton.place(x=300, y=57)

        """ AMAZON AREA """
        # Amazon Frame
        amz = tk.Frame(
            self,
            bg="#9fbfdf",
            height=300,
            width=900,
            bd=1,
            relief=tk.SUNKEN,
            borderwidth=5,
        )
        # flip.pack(fill=tk.X, padx=5, pady=5)
        amz.place(x=10, y=330)

        # Amazon product label
        amzProductLabel = tk.Label(
            amz, text="Product : ", font=controller.mediumBoldFont
        )
        amzProductLabel.place(x=10, y=120)

        # Reading the saved CSV file
        amzColnames = ["Product", "Price", "Rating"]
        amzData = pd.read_csv("amz.csv", names=amzColnames)

        # Assigning columns from CSV to variables
        amzProducts = amzData.Product.tolist()
        amzPrices = amzData.Price.tolist()
        amzRatings = amzData.Rating.tolist()

        # Variable which points to the selected option in dropdown menu
        amzOptionVar = tk.StringVar(amz)
        # Setting the first element of flipProducts as selected option
        amzOptionVar.set(amzProducts[0])

        # Products dropdown menu
        amzOptions = tk.OptionMenu(amz, amzOptionVar, *amzProducts)
        amzOptions.place(x=120, y=117)

        # Price Label
        amzPriceLabel = tk.Label(amz, text="Price : ", font=controller.smallBoldFont)
        amzPriceLabel.place(x=10, y=160)

        # Rating Label
        amzRatingLabel = tk.Label(amz, text="Rating : ", font=controller.smallBoldFont)
        amzRatingLabel.place(x=150, y=160)

        # TODO: Test price and rating fetch
        def onAmzOptionSelected():
            # Getting the product selected and its index in the products array
            selectedProduct = amzOptionVar.get()
            indexOfSelectedProduct = amzProducts.index(selectedProduct)

            # Getting price from the prices list and setting the label text
            priceOfSelectedProduct = str(amzPrices[indexOfSelectedProduct])
            amzPriceLabel.config(text="Price : " + priceOfSelectedProduct)

            # Getting rating from the ratings list and setting the label text
            ratingOfSelectedProduct = amzRatings[indexOfSelectedProduct]
            amzRatingLabel.config(text="Rating : " + ratingOfSelectedProduct)

        # Visit page button
        visitAmzButton = tk.Button(
            amz, text="Check price and rating", command=onAmzOptionSelected
        )
        visitAmzButton.place(x=300, y=157)

    # def __showOptions(self):
    #     amzVar = tk.StringVar(self)
    #     amzVar.set(amzData["products"][0])

    #     amzOptions = tk.OptionMenu(self, amzVar, *amzData["products"])
    #     amzOptions.pack()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self, text="This is the start page", font=controller.largeBoldFont
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
        label = tk.Label(self, text="This is page 1", font=controller.largeBoldFont)
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
        label = tk.Label(self, text="This is page 2", font=controller.largeBoldFont)
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
