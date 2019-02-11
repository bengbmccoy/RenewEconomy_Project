'''
Author: Ben McCoy
Date started: 2019-01-12

This is the second script of the Renewecon project, this script will be the
so called "reader and ranker".

This script will do the following:
- Take arguemnts from the command line as to what to do --> DONE
- Print a list of new urls, based on command line arguemnt --> DONE
- Print a list of all urls, based on command line argument --> DONE
- Print a list of unread urls, based on command line argument --> DONE
- Print a list of read urls, based on command line argument --> DONE
- Print a list of urls ordered by rank, based on command line argument --> DONE
- Allow the user to select a file to be read, based on command line
    argument --> DONE
- Open the file in a chrome browser --> DONE
- Allow the user to rank an article (no idea how to do this!)
- Accept or ammend the articles rank

***TODO***
- Currently I cannot pass an optional interger argument that would represent
a site's ID number. Currently you are required to put a 0 as the ID number in
order to perform no action.
I would like to be able to leave an argument blank, but if the argument is there
it will be an interger of the ID of the article to open.
I also need some method of allowing a user of the script to rank an artice!

'''

import pandas as pd
import numpy as np
import datetime
import webbrowser
import argparse
import webbrowser


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
    parser.add_argument('-v', '--viewer',
                        help='allows user to select and view and article',
                        action='store_true')
    parser.add_argument('id', type=int,
                        default=False,
                        help='input the ID of an article to be viewed, put 0 to not open any new tabs')
    args = parser.parse_args()

    url_database = fetch_url_database()
    # print url_database
    print "url_database collected"

    if args.new:
        new_urls = get_list_new(url_database, 7) # 7 to be used as place holder for arg parse
        for i in new_urls:
            print i
        print "new urls collected"

    if args.all:
        all_urls = get_list_all(url_database)
        for i in all_urls:
            print i
        print "all urls collected"

    if args.unread:
        unread_urls = get_list_unranked(url_database)
        for i in unread_urls:
            print i
        print 'unranked urls collected'

    if args.read:
        read_urls = get_list_ranked(url_database)
        for i in read_urls:
            print i
        print 'read and ranked urls collected'

    if args.order:
        rank_url_db = get_rank_url_db(url_database)
        print rank_url_db.loc[:, 'Title':'Rank']
        print 'ranked urls collected and ordered'

    # if args.viewer:
    if args.id > 0:
        id_num = str(args.id)
        for i in range(len(url_database.index)):
            if str(url_database.at[i,'Title'][-5:]) == id_num:
                # open_chrome_tab(url_database.at[i, 'URL'])
                open_chrome_tab(url_database.at[i, 'Title'])



def open_chrome_tab(url):
    url = 'file:///C:/Users/benja/_repo_home/pages_/' + url + '.html'
    webbrowser.open_new_tab(url)

def get_rank_url_db(url_database):
    # Returns an ordered pandas database with the titles ordered from highest
    # to lowest ranked. Articles not ranked will not be included.

    rank_db = url_database.loc[url_database['Rank'] > 0]
    rank_db.is_copy = False # Disables the SettingWithCopyWarning
    rank_db.sort_values('Rank', inplace=True, ascending=False)
    return rank_db

def get_list_ranked(url_database):
    # Returns a list of titles that have a rank that is non-numerical

    ranked_urls = []
    for i in range(len(url_database.index)):
        if url_database.at[i, 'Rank'] >= 0:
            ranked_urls.append(url_database.at[i, 'Title'])

    return ranked_urls

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
        if abs((current_date - datetime.datetime.strptime(row['Date'],
        '%Y-%m-%d').date()).days) < days_new:
            new_urls.append(row['Title'])

    return new_urls

def fetch_url_database():

    # fetches 'url_database.csv' as read and write and returns pandas db
    url_database = pd.read_csv('url_database.csv')
    return url_database

main()
