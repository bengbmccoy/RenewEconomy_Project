'''
Author: Ben McCoy
Date started: 2019-01-04

This is my first github project.
I will create a webscraper that can access RenewEconomy once a day and search
for articles. Any new articles will be scraped, stored locally, read, analysed
and ranked by myslef.

The idea is to practice using github, and perhaps build a database of articles
to use statistical methods and other fun tools on.

This script will be the scraper of this project (see readme.md), this will be
scheuled to run daily, or so. This script will do the following:

- Open existing article database record --> DONE
- Access the RenewEconomy homepage --> DONE
- Scrape the page --> DONE
- Search and store for artile links --> DONE
- Cross reference searching for new articles
- Go through list of new articls and open web page:
- Scarpe the page
- Parse the article text
- Save the article text and meta data

'''

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def main():

    #print 'hello world'

    url_database = fetch_url_database()
    # print url_database
    print 'url_database opened'

    main_page = get_main_page_soup()
    # print main_page
    print 'main page soup collected'

    url_list = set(search_soup_urls(main_page))
    # print url_list
    print 'urls of articles collected'



    # save_url_database(url_database)
    # print 'url_database saved'

def search_soup_urls(soup):

    # This function takes the soup of a URL and finds any links to
    # other pages on the RenewEconomy site main page.
    # The function returns a list of all URLs found.
    # The funtion isloate_urls takes the string from the soup and isoloates
    # the urls.
    # Example url: 'https://reneweconomy.com.au/all-we-want-for-christmas-four-disruptors-share-their-2019-energy-policy-wishes-61100'
    url_list = []
    soup = str(soup)
    strings = soup.split()

    for string in strings:
        if 'https:' in string and string[-6:-2].isdigit() is True:
            url_list.append(string)

    url_list = isolate_urls(url_list)

    return url_list

def isolate_urls(strings):

    # Splints urll out of the strinf through HARD CODE, this needs to be made
    # more robust in the future.
    # Returns a list of clean urls
    url_list = []
    for string in strings:
        try:
            start = 'href="'
            end = '/"'
            # print((string.split(start))[1].split(end)[0])
            url_list.append(((string.split(start))[1]).split(end)[0])
        except:
            pass

    return url_list

def get_main_page_soup():
    # This function returns the html of the website listed
    url = "http://reneweconomy.com.au/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml') #parse the HTML as a string
    return soup

def new_url_database():

    # fetches 'url_database.csv' as read and write and returns pandas db
    url_database = pd.DataFrame(np.nan, index=[], columns=['URL', 'ID', 'Date', 'Title', 'Author'])
    url_database = url_database.fillna(0)
    return url_database

def fetch_url_database():

    # fetches 'url_database.csv' as read and write and returns pandas db
    url_database = pd.read_csv('url_database.csv')
    return url_database

def save_url_database(url_database):
    # saves the pandas database as a csv in the same directory
    url_database.to_csv("url_database.csv", encoding='utf-8', index=False)

main()
