'''
Author: Ben McCoy
Date started: 2019-01-12

This is the second script of the Renewecon project, this script will be the
so called "reader and ranker".

This script will do the following:
- Take arguemnts from the command line as to what to do
- Print a list of new urls, based on command line arguemnt --> DONE
- Print a list of all urls, based on command line argument --> DONE
- Print a list of unread urls, based on command line argument --> DONE
- Print a list of read urls, based on command line argument
- Print a list of urls ordered by rank, based on command line argument
- Allow the user to select a file to be read, based on command line argument
- Open the file in a chrome browser
- Accept or ammend the articles rank

'''

import pandas as pd
import numpy as np
import datetime
import webbrowser
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new',
                        help='displays any articles downloaded in the 7 days',
                        action='store_true')
    parser.add_argument('-a', '--all',
                        help='displays all articles saved',
                        action='store_true')
    parser.add_argument('-u', '--unread',
                        help='displays all unread artices',
                        action='store_true')
    parser.add_argument('-r', '--read',
                        help='displays all read articles',
                        action='store_true')
    parser.add_argument('-o', '--order',
                        help='displays artciles ordered from high to low rank',
                        action='store_true')
    args = parser.parse_args()

    url_database = fetch_url_database()
    # print url_database
    print "url_database collected"

    if args.new:
        new_urls = get_list_new(url_database, 7) # 7 to be used as place holder for arg parse
        print new_urls
        print "new urls collected"

    if args.all:
        all_urls = get_list_all(url_database)
        print all_urls
        print "all urls collected"

    if args.unread:
        unread_urls = get_list_unranked(url_database)
        print unread_urls
        print 'unranked urls collected'

def open_chrome_tab(url):
    '''
    THis section is todo
    '''

def get_list_unranked(url_database):
    # Returns a list of urls that have no rank

    unranked_urls = []
    for i in range(len(url_database.index)):
        if url_database.at[i, 'Rank'] != int:
            unranked_urls.append(url_database.at[i, 'Title'])

    return unranked_urls

def get_list_all(url_database):
    # Reurns a list of all urls stored

    return url_database['URL'].tolist()

def get_list_new(url_database, days_new):
    # Returns a list of new urls added in the past 7 days.
    # In the future they need also be unranked?

    days_new = 7 # to be used as a place holder for when arg parse is available
    new_urls = []
    current_date = datetime.datetime.now().date()
    # for date in url_database['Date'].tolist():
    for index, row in url_database.iterrows():
        if abs((current_date - datetime.datetime.strptime(row['Date'], '%Y-%m-%d').date()).days) < days_new:
            new_urls.append(row['URL'])

    return new_urls

def fetch_url_database():

    # fetches 'url_database.csv' as read and write and returns pandas db
    url_database = pd.read_csv('url_database.csv')
    return url_database

main()
