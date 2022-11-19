# import package from pip
import csv
import re
import os.path
import requests
from art import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import shutil
# /import package from pip

# welcome message
tprint("OpenClassrooms", "black_bubble")
tprint("P2_DA Python", "black_bubble")
print("\n")
# /welcome message

# folder for the csv files creation
directory = "data_extracted/csv"
if os.path.exists(directory):
    print("Folder needed for scrapping data already exist:", "Folder name :", directory)
if not os.path.exists(directory):
    os.makedirs(directory)
    print("Folder as been created for scrapping the website data:", "Folder name:", directory)
print("\n")
# /folder for the csv files creation

# folder for the pics files creation
directory = "data_extracted/pics/"
if os.path.exists(directory):
    print("Folder needed for scrapping img already exist:", "Folder name :", directory)
if not os.path.exists(directory):
    os.makedirs(directory)
    print("Folder as been created for scrapping the website img:", "Folder name:", directory)
print("\n")
# /folder for the pics files creation

# get soup from main url
url3 = "https://books.toscrape.com/index.html"
requests.get(url3)
response3 = requests.get(url3)
# online?
if response3.status_code != 200:
    print("bad URL")
else:
    print("The website to scrap is online:", response3)
    print("Be patient for all the files creation now :)")
    print("\n")
    # /online?
# use of beautifulsoup
soup3 = BeautifulSoup(response3.content, "html.parser")
# /use of beautifulsoup
# /get soup from main url

# list of all categories url
li_category = []
# / list of all categories url


# function to get all the categories url from the main page
def get_url_category():
    global li_category
    for cat in soup3.findAll("a"):
        li_category.append(urljoin(url3.rstrip(), cat.get("href")))
    return li_category


get_url_category()
# function to get all the categories url from the main page

# remove the useless url from the categories url list
del li_category[0:3]
del li_category[50:100]
# / remove the useless url from the categories url list

# get soup from category url
for category in li_category:
    url2 = category
    # online url?
    requests.get(url2)
    response2 = requests.get(url2)
    # use of beautifulsoup
    soup2 = BeautifulSoup(response2.content, "html.parser")
    # /use of beautifulsoup
# /get soup from category url

    # list of all url on one category's page
    books_category = []
    # list of all url on one category's page

    # buckle to fill the books_category
    while True:
        li_books = []

        # function to get the url of the books from one category
        def get_url_books():
            global li_books
            for link in soup2.find_all('h3'):
                li_books.append(urljoin(url2,
                                        link.find("a").get("href")))
            return li_books

        get_url_books()
        # /function to get the url of the books from one category

        # get soup from one book url
        for books in li_books:
            url = books
            # /website to scrap
            # online url?
            requests.get(url)
            response = requests.get(url)
            # use of beautifulsoup
            soup = BeautifulSoup(response.content, "html.parser")
            # /use of beautifulsoup
            # /get soup from one book url

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

            # creation of all the pictures
            r = requests.get(value_url, stream=True)
            with open(directory + category + "_" + re.sub("[^a-zA-Z0-9]+", "", title) + "_" + time.strftime("%Y-%m-%d") + ".jpg",
                      "wb") as pic_dl:
                shutil.copyfileobj(r.raw, pic_dl)
                # /creation of all the pictures

            books_category.append(description)
            # /get all needed information to create the csv file

        # is there another page?
        next_page = soup2.find("li", {"class": "next"})
        if next_page is not None:
            next_page = next_page["class"]
            li = soup2.find("li", {"class": "next"})
            url2 = urljoin(url2.rstrip(),
                           li.find("a").get("href"))
            requests.get(url2)
            response2 = requests.get(url2)
            # use of beautifulsoup
            soup2 = BeautifulSoup(response2.content, "html.parser")
            # /use of beautifulsoup
        else:
            break
            # /is there another page?
    # buckle to fill the books_category

    # create the csv file with the headers and the descriptions
    csv_name = "data_extracted/csv/" + time.strftime("%Y-%m-%d") + "_" + category + ".csv"
    with open(csv_name, "w", encoding='UTF8', newline='') as data_csv:
        writer = csv.writer(data_csv, delimiter=";")
        # gives the header name row into csv
        writer.writerow(['product_page_url', 'title', 'upc', 'price_including_tax', "price_excluding_tax",
                         "number_available",
                         "product_description", "category", "review_rating", "image_url"])
        # data add in csv file
        writer.writerows(books_category)

        if True:
            print("A new file has been created :", csv_name)
            print("You can open this file with a csv software now")
            print("All pictures of :" + category + " has been downloaded")
    # /create the csv file with the headers and the descriptions
