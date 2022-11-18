# import from pip
import csv
import re
import os.path
import requests
from art import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# /import from pip

# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")
print("\n")
# /welcome message

# folder for the csv file creation
directory = "data_extracted"
if os.path.exists(directory):
    print("Folder needed for scrapping already exist:", "Folder name :", directory)
if not os.path.exists(directory):
    os.mkdir(directory)
    print("Folder as been created for scrapping the website data:", "Folder name:", directory)
print("\n")
# /folder for the csv file creation

# website to scrap
url2 = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
# /website to scrap
requests.get(url2)
response2 = requests.get(url2)
if response2.status_code != 200:
    print("bad URL")
else:
    print("The website to scrap is online:", response2)
    print("\n")
    # /online?
# use of beautifulsoup
soup2 = BeautifulSoup(response2.content, "html.parser")
# /use of beautifulsoup

next_page = soup2.find("li", {"class": "next"})
next_page = next_page["class"]
li = soup2.find("li", {"class": "next"})

print(next_page)
while next_page:
    url2 = urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html".rstrip(),
                   li.find("a").get("href"))
    requests.get(url2)
    response2 = requests.get(url2)
    # use of beautifulsoup
    soup2 = BeautifulSoup(response2.content, "html.parser")
    # /use of beautifulsoup

    next_page = soup2.find("li", {"class": "next"})
    if next_page is not None:
        next_page = next_page["class"]
    li = soup2.find("li", {"class": "next"})

li_books = []


# Get the list of the book from one category
def get_url_books():
    global li_books
    for link in soup2.find_all('h3'):
        li_books.append(urljoin("https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html",
                                link.find("a").get("href")))
    return li_books
# /Get the list of the book from one category


get_url_books()


books_category = []


# website to scrap
for books in li_books:
    url = books
    # /website to scrap
    # online url?
    requests.get(url)
    response = requests.get(url)
    # use of beautifulsoup
    soup = BeautifulSoup(response.content, "html.parser")
    # /use of beautifulsoup

    # Variables with soup to extract information needed
    tr = soup.findAll("tr")
    p = soup.findAll("p")
    a = soup.findAll("a")
    # /Variables with soup to extract information needed

    # get all needed information to create the csv file
    description = []

    product_page_url = url
    description.append(product_page_url)

    title = soup.find("h1").string
    description.append(title)

    upc = tr[0].td.string
    description.append(upc)

    price_including_tax = tr[2].td.string
    price_including_tax = re.sub('[^0-9.]+', '', price_including_tax)
    description.append(price_including_tax)

    price_excluding_tax = tr[3].td.string
    price_excluding_tax = re.sub('[^0-9.]+', '', price_excluding_tax)
    description.append(price_excluding_tax)

    number_available = tr[5].td.string
    description.append(number_available)

    product_description = p[3].string
    description.append(product_description)

    category = a[3].string
    description.append(category)

    review_rating = soup.find("p", {"class": "star-rating"})
    review_rating = review_rating["class"]
    if "One" in review_rating:
        review_rating = "1"
    elif "Two" in review_rating:
        review_rating = "2"
    elif "Three" in review_rating:
        review_rating = "3"
    elif "Four" in review_rating:
        review_rating = "4"
    elif "Five" in review_rating:
        review_rating = "5"
    description.append(review_rating)

    image_url = soup.find_all("img")
    image_url = image_url[0].get("src")
    value_url = "http://books.toscrape.com/" + image_url
    description.append(value_url)
    # /get all needed information to create the csv file
    books_category.append(description)

# create the csv file with the headers and the descriptions
with open("data_extracted/data.csv", "w", encoding='UTF8', newline='') as data_csv:
    writer = csv.writer(data_csv, delimiter=";")
    # gives the header name row into csv
    writer.writerow(['product_page_url', 'title', 'upc', 'price_including_tax', "price_excluding_tax",
                     "number_available",
                     "product_description", "category", "review_rating", "image_url"])
    # data add in csv file
    writer.writerows(books_category)

    if True:
        print("All the data has been scrapped in the folder: data_extracted")
        print("The file name is : data.csv")
        print("You can open the file with a csv software now")
# /create the csv file with the headers and the descriptions
