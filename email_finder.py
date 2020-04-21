#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Google search
from googlesearch import search

# Requests, html and searches utils
import re
import requests
from bs4 import BeautifulSoup

# Database utils
import sqlite3
from sqlite3 import Error

TITLE = """
  ______  __  __            _____  _        ______  _____  _   _  _____   ______  _____  
 |  ____||  \/  |    /\    |_   _|| |      |  ____||_   _|| \ | ||  __ \ |  ____||  __ \ 
 | |__   | \  / |   /  \     | |  | |      | |__     | |  |  \| || |  | || |__   | |__) |
 |  __|  | |\/| |  / /\ \    | |  | |      |  __|    | |  | . ` || |  | ||  __|  |  _  / 
 | |____ | |  | | / ____ \  _| |_ | |____  | |      _| |_ | |\  || |__| || |____ | | \ \ 
 |______||_|  |_|/_/    \_\|_____||______| |_|     |_____||_| \_||_____/ |______||_|  \_\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
"""


def _make_a_google_query(query):
    """
    :param query: The query to make in google
    :return: It returns a list with the resultant web pages of the query
    """
    print("[!] Making the google query: {} ".format(query))
    my_webs_page_result_list = []
    for i in search(query,  # The query you want to run
                    tld='com',  # The top level domain
                    lang='en',  # The language
                    num=100,  # Number of results per page
                    start=0,  # First result to retrieve
                    stop=500,  # Last result to retrieve
                    pause=2.0,  # Lapse between HTTP requests
                    ):
        my_webs_page_result_list.append(i)
    print("[!] DONE")
    return my_webs_page_result_list


def _fist_level_email_finder(url, emails_set):
    """
    :param url: The URL where it is going to search
    :return: It return the emails found
    """

    # Html finder
    try:
        r = requests.get(url)
    except:
        return emails_set

    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # Title finder
    try:
        title = soup.title.text.replace("\n", "").replace("\t", "")
    except:
        title = None

    # Email finder in the first page
    first_email_search_filter = soup.find_all(href=re.compile("mailto"))
    if len(first_email_search_filter) > 0:
        for i in first_email_search_filter:
            if i.string != None and "@" in i.string:
                i.string = i.string.replace("\t", "").replace("\n", "").replace(" ", "")
                email = i.string
                print(url, title, email)
                emails_set.add((url, title, email))
            else:
                href_email = i.attrs.get('href', None)
                if href_email != None and "@" in href_email:
                    email_string = href_email.replace("\t", "").replace("\n", "").replace(" ", "").replace("mailto:",
                                                                                                           "").replace("?subject=", "").replace("?", "")
                    email = email_string
                    print(url, title, email)
                    emails_set.add((url, title, email))
    return emails_set


def _second_level_email_finder(url, emails_set, pattern):
    """
    :param url: The URL where it is going to search
    :param pattern: The pattern for considering a link relevant for the search
    :return: It go to the found links that contains a given pattern and makes a first_level search in the found link
    """
    hrefs_set = set()

    # Html finder
    try:
        r = requests.get(url)
    except:
        return emails_set

    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    second_email_search_filter = soup.find_all(href=re.compile(pattern))

    for pattern_match in second_email_search_filter:
        # Obtained list is inserted in a set for avoiding duplications
        hrefs_set.add(pattern_match['href'])

    if len(hrefs_set) > 0:
        for link in hrefs_set:
            if ".html" in url:
                url = '/'.join(url.split("/")[:-1])

            if not "http" in link:
                emails_set = _insert_found_emails(emails_set, _fist_level_email_finder(url + link, emails_set))
            else:
                emails_set = _insert_found_emails(emails_set, _fist_level_email_finder(link, emails_set))

    return emails_set


def _insert_found_emails(emails_set, new_emails_set):
    for new_email in new_emails_set:
        print(new_email)
        emails_set.add(new_email)
    return emails_set


def main():
    print(TITLE)
    emails_set = set()

    query_results = _make_a_google_query("'Colmenar Viejo' AND restaurantes")

    print("[!] Getting the web emails")
    for web_page in query_results:
        # try:
        # First level email finder
        emails_set = _insert_found_emails(emails_set, _fist_level_email_finder(web_page, emails_set))

        # Second level email finder if it found more links to what I am looking for
        emails_set = _insert_found_emails(emails_set, _second_level_email_finder(web_page, emails_set, "/Restaurant"))
        emails_set = _insert_found_emails(emails_set, _second_level_email_finder(web_page, emails_set, "/restaurant"))

        # except:
        #     pass


    for email in emails_set:
        print(email)

    print("[!] DONE, {} emails found".format(len(emails_set)))

    # Create a database connection to a SQLite database and insert the elements
    print("[!] Inserting in DB")

    conn = None
    try:
        conn = sqlite3.connect("emails_database.db")  # Create db connection
        cur = conn.cursor()

        cur.execute(" CREATE TABLE IF NOT EXISTS emails(web text, title text, email text)")  # Create emails table
        conn.commit()

        i = 1
        for email in emails_set:
            cur.execute("INSERT INTO emails VALUES(?, ?, ?)", (email[0], email[1], email[2]))
            conn.commit()
            i += 1
        print("[!] DONE")

    except Error as e:
        print("[X] Error inserting elements in database")
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
