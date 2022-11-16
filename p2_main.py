# import from pip
import csv
import os.path
import requests
from art import *
from bs4 import BeautifulSoup
# /import from pip

# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")
print("\n")
# /welcome message

# website to scrap
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
url2 = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
# /website to scrap

# online url?
requests.get(url)
response = requests.get(url)
if response.status_code != 200:
    print("bad URL")
else:
    print("The website to scrap is online:", response)
    print("\n")
requests.get(url2)
response2 = requests.get(url2)
if response2.status_code != 200:
    print("bad URL")
else:
    print("The website to scrap is online:", response2)
    print("\n")
    # /online?

# use of beautifulsoup
soup = BeautifulSoup(response.content, "html.parser")
soup2 = BeautifulSoup(response2.content, "html.parser")
# /use of beautifulsoup

# get all the book titles in a list
"""def books_title():"""
# /get all the book titles in a list

# folder for the csv file creation
directory = "data_extracted"
if os.path.exists(directory):
    print("Folder needed for scrapping already exist:", "Folder name :", directory)
if not os.path.exists(directory):
    os.mkdir(directory)
    print("Folder as been created for scrapping the website data:", "Folder name:", directory)
print("\n")
# /folder for the csv file creation

# csv file information
csv.field_size_limit(10)
header = ['product_page_url', 'upc', 'title', 'price_including_tax', "price_excluding_tax", "number_available",
          "product_description", "category", "review_rating", "image_url"]
description = []
# /csv file information

# Variables with soup to extract information needed
tr = soup.findAll("tr")
p = soup.findAll("p")
a = soup.findAll("a")
# /Variables with soup to extract information needed


# get all needed information to create the csv file
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
# /get all needed information to create the csv file


def get_url_books():
    li_books = [soup.findAll("a", {"class": "image_container"})]
    print(li_books)


get_url_books()


# create the csv file with the headers and the descriptions
def csv_creation():
    with open("data_extracted/data.csv", "w", encoding='UTF8', newline='') as data_csv:
        writer = csv.writer(data_csv, delimiter=";")
        # gives the header name row into csv
        writer.writerow(header)
        # data add in csv file
        writer.writerow(description)
        if True:
            print("All the data has been scrapped in the folder: data_extracted")
            print("The file name is : data.csv")
            print("You can open the file with a csv software now")


csv_creation()
# /create the csv file with the headers and the descriptions
