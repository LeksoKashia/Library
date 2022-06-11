import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randrange
import sqlite3
# page = 1
# while page < 2:
#     t12 = ()
#     tuple12 = ()
#     book_href_list = []
#     book_list = []
#
#     url = 'https://biblusi.ge/products?category=291&category_id=309&page=' + str(page)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     sub_soup = soup.find('div', class_="row")
#     books = sub_soup.find_all('div', class_="mb-1_875rem col-sm-4 col-md-3 col-xl-2 col-6")
#
#     for each in books:
#         img_url = each.a.div.attrs.get('style').strip("background-image:url('")[:-3]
#         book = each.div.acronym.text
#         price = each.find('div', class_='text-primary font-weight-700').text
#         price = price.replace(' ', '').replace('\n', '')
#         book_url = each.a.get('href')
#         tuple1 = tuple12+(book,)
#         tuple2 = tuple1+(price,)
#         tuple3 = tuple2+(img_url,)
#         tuple4 = tuple3+('https://biblusi.ge'+book_url,)
#         book_list.append(tuple4)
#     page += 1

url = "https://www.biblusi.ge/search-result?q=%E1%83%9B%E1%83%9D%E1%83%A0%E1%83%A2%E1%83%9E%E1%83%9D%E1%83%A5%E1%83%A2%E1%83%9D%E1%83%9154%E1%83%9254&page=1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
sub_soup = soup.find('div',class_="shadow p-5 mb-5 bg-white rounded")
error = sub_soup.find_all('h3')
print(error)
print(str(error)[44:67])