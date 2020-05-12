import requests
from bs4 import BeautifulSoup
import pandas as pd

products = []
prices = []
ratings = []

url = "https://www.amazon.in/s?k="
search_input = input("Enter product name : ").replace(" ", "+")

link = "https://www.amazon.in/s?k=apple+mobile" + search_input + "&ref=nb_sb_noss_2"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

source = requests.get(link, headers=headers)
content = source.text
soup = BeautifulSoup(content, "lxml")
products_class = "sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"

for a in soup.findAll("div", attrs={"class": products_class}):

    try:
        name = a.find(
            "span", attrs={"class": "a-size-medium a-color-base a-text-normal"}
        )
        products.append(name.text[:60])

        try:
            price = a.find("span", attrs={"class": "a-price-whole"})
            # or a-offscreen for price with rupee symbol
            prices.append(int(price.text.replace(",", "")))
        except AttributeError:
            prices.append("Not available")

        try:
            rating = a.find("span", attrs={"class": "a-icon-alt"})
            ratings.append(rating.text[:3])
        except AttributeError:
            ratings.append("Not available")

    except AttributeError:
        continue

df = pd.DataFrame(
    {"Product_Name": products, "Price (in Rs)": prices, "Rating (out of 5)": ratings}
)
df.to_csv("amz.csv", index=False, encoding="utf-8")
