# import from pip
import csv
import os.path
import requests
from art import *
from bs4 import BeautifulSoup

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

# folder for the csv file creation
directory = "data_extracted"
if not os.path.exists(directory):
    os.mkdir(directory)

# csv file informations
csv.field_size_limit(10)
header = ['product_page_url', 'upc', 'title', 'price_including_tax', "price_excluding_tax", "number_available",
          "product_description", "category", "review_rating", "image_url"]
description = []

# Variables with soup to extract information needed
tr = soup.findAll("tr")
p = soup.findAll("p")
a = soup.findAll("a")


# Get all needed information to create the csv file
def des():
    product_page_url = url
    description.append(product_page_url)
    title = soup.find("h1").string
    description.append(title)
    upc = tr[0].td.string
    description.append(upc)
    price_including_tax = tr[2].td.string
    description.append(price_including_tax)
    price_excluding_tax = tr[3].td.string
    description.append(price_excluding_tax)
    number_available = tr[5].td.string
    description.append(number_available.string)
    product_description = p[3].string
    description.append(product_description)
    category = a[3].string
    description.append(category)
    review_rating = soup.find("p", {"class": "star-rating Three"})
    review_rating = review_rating["class"]
    description.append(review_rating)
    image_url = soup.find_all("img")
    image_url = image_url[0].get("src")
    value_url = ["http://books.toscrape.com/" + image_url]
    description.append(value_url)


des()

# create the csv file with the headers and the descriptions
with open("data_extracted/data.csv", 'w') as data_csv:
    # Créer un objet writer (écriture) avec ce fichier
    writer = csv.writer(data_csv, delimiter=';')
    writer.writerow(header)
print("All the data has been scrapped in the folder: extracted_data")
print("The file name is : data.csv")
