# import from pip
import csv
from art import *
from bs4 import BeautifulSoup
import requests

# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")
print("\n")

# website to scrap
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# online?
requests.get(url)
response = requests.get(url)
if response.status_code != 200:
    print("bad URL")
else:
    print("The website to scrap is online:", response)

# Get the html of the website into a variable
html = response.content
soup = BeautifulSoup(html, "html.parser")
print("\n")

# Variables with soup to extract information needed
tr = soup.findAll("tr")
p = soup.findAll("p")
a = soup.findAll("a")
# Get all needed information to create the csv file
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
review_rating = soup.find("p", {"class": "star-rating Three"})
review_rating = review_rating["class"]
print(review_rating)
image_url = soup.find_all("img")
image_url = image_url[0].get("src")
value_url = ["http://books.toscrape.com/" + image_url]
print(value_url)

# csv file creation
csv.field_size_limit(10)
header = ['product_page_url', 'upc', 'title', 'price_including_tax', "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
writer = csv.writer(f)
f.close()
