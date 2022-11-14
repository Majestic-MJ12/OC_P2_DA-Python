# import from pip
import requests
from bs4 import BeautifulSoup
from art import *


# welcome message
tprint("OpenClassrooms", "white_bubble")
tprint("P2_DA Python", "white_bubble")

# website to scrap
url = "http://books.toscrape.com/"

# website response
response = requests.get(url)
print("Site Web en ligne ? :", response)
