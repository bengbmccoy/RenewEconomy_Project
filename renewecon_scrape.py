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

- Open existing article database record
- Access the RenewEconomy homepage
- Scrape the page
- Search and store for artile links
- Cross reference searching for new articles
- Go through list of new articls and open web page:
- Scarpe the page
- Parse the article text
- Save the article text and meta data

'''

import pandas as pd
import numpy as np

def main():

    #print 'hello world'

    url_database = fetch_url_database()
    print 'url_database opened'

    print url_database



    # save_url_database(url_database)
    # print 'url_database saved'



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
