# import from pip
from art import *
from bs4 import BeautifulSoup
import requests
import re

# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")
print("\n\n")

# website to scrap
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
# online?
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, "html.parser")

tr = soup.findAll("tr")
p = soup.findAll("p")
a = soup.findAll("a")

product_page_url = url
print(product_page_url)
title = soup.find("h1")
print(title.string)
upc = tr[0].td.string
print(upc)
price_including_tax = tr[2].td.string
print(price_including_tax)
price_excluding_tax = tr[3].td.string
print(price_excluding_tax)
number_available = tr[5].td.string
print(number_available.string)
product_description = p[3].string
print(product_description)
category = a[3].string
print(category)

if re.match("star-rating One", html):
    review_rating = 1
elif re.search("star-rating Two", html):
    review_rating = 2
elif re.search("star-rating Three", html):
    review_rating = 3
elif re.search("star-rating Four", html):
    review_rating = 4
elif re.search("star-rating Five", html):
    review_rating = 5
print(review_rating)

image_url = soup.find("img")
print(image_url)



