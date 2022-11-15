# import from pip
from art import *
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")
print("\n\n")

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)

if response.ok:
    product_alone = []
    soup = BeautifulSoup(response.text, "html.parser")
    product_page_url = url
    universal_product_code = soup.findAll("tbody", "tr", "td")
    title = soup.findAll("h1")
    price_including_tax = soup.findAll("tbody", "tr", "td")
    product_alone.append(price_including_tax)


print(product_alone)
