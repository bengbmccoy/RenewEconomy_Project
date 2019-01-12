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
- Cross reference searching for new articles --> DONE
- Go through list of new articls and open web page --> DONE
- Scarpe the page --> DONE
- Parse the article text --> DONE
- Save the article text and meta data --> DONE
- Record the saving of any new articles --> DONE

'''

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import datetime

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

    new_urls = check_new_urls(url_list, url_database)
    # print new_urls
    print 'new urls collected from main page'

    # new_urls = new_urls[:1] # This is to reduce runtime during debugging
    saved_urls = save_new_articles(new_urls, url_database)
    # print saved_urls
    print url_database
    print 'articles saved as HTML pages_, meta data saved in url_database.csv'



    # save_url_database(url_database)
    # print 'url_database saved'

def save_urls_to_db(saved_urls, url_database):
    # adds a new line to the url_database with the info attached
    pass

def get_filename(url):
    # Extractes the URL, current date, url_ID and title, it then
    # places it in a list to be returned

    return url.split('/')[3]

def save_new_articles(new_urls, url_database):

    # This function takes a list of URLs and parses and stores them
    saved_urls = []
    for url in new_urls:
        try:
            file_name = url.split('/')[3]
            url_title = file_name
            print 'saving ' + file_name
            file_name = 'pages_/' + file_name + '.html'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml') #parse the HTML as a string
            url_author = get_author(soup)
            url_date = datetime.datetime.now().date()
            with open(file_name, 'w') as file:
                file.write(str(soup))
            saved_urls.append(url)
            save_meta_data(url_database, url, str(url_date), url_title, url_author)
        except:
            print 'failed to save ' + url

    return saved_urls

def save_meta_data(url_database, url, url_date, url_title, url_author):
    # save the meta data to the url_database

    info = [url, str(url_date), url_title, url_author]
    url_database.loc[(len(url_database.index))] = info
    save_url_database(url_database)

def get_author(soup):
    # print soup
    author_str = (str(soup.find_all(class_="author-link")))
    author = author_str.split('rel="author">')[1][2:-6]
    return author

def check_new_urls(url_list, url_database):

    # This function will check any URLs found on the main page of RenewEconomy
    # against the already saved URLs previously stored

    old_urls = url_database['URL'].tolist()
    new_urls = list(set(url_list) - set(old_urls))

    return new_urls

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
