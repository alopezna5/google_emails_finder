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


class email_finder():

    def __init__(self, query, db_name, paginate):
        self.query = query
        self.db_name = db_name
        self.paginate = True if paginate is not None else False


    def _make_a_google_query(self, query):
        """
        :param query: The query to make in google
        :return: It returns a list with the resultant web pages of the query
        """
        print("[!] Making the google query: {} ".format(query))
        my_webs_page_result_list = []
        for i in search(query,  # The query you want to run
                        lang='en',  # The language
                        num_results=6000  # Number of results per page
                        ):
            my_webs_page_result_list.append(i)
        print("[!] DONE")
        return my_webs_page_result_list


    def __initialize_db(self):
        """
        :return: It initializes the database
        """
        print("[!] Initializing database")
        conn = sqlite3.connect(self.db_name + ".db")  # Create db connection
        cur = conn.cursor()
        cur.execute(
            " CREATE TABLE IF NOT EXISTS emails(web text, title text, email text, PRIMARY KEY(email))")  # Create emails table
        conn.commit()
        conn.close()
        print("[!] DONE!")


    def _insert_tuple(self, tuple):
        """
        :param tuple: The tuple to insert in the sets self.results_set
        :return: If the email (primary key) does not exists, it insert the tuple in self.results_set
        """

        print("[!] Inserting in DB")
        conn = None
        try:
            conn = sqlite3.connect(self.db_name + ".db")  # Create db connection
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO emails VALUES(?, ?, ?)", (tuple[0], tuple[1], tuple[2]))
                conn.commit()
            except:
                print("{} not inserted due the email is already stored".format(tuple))
        except Error as e:
            print("[X] Error inserting elements in database")
            print(e)
        finally:
            if conn:
                conn.close()


    def _fist_level_email_finder(self, url):
        """
        :param url: The URL where it is going to search
        :return: It returns the emails found
        """

        # Html finder
        try:
            r = requests.get(url)
        except:
            return False

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
                    self._insert_tuple((url, title, email))
                else:
                    href_email = i.attrs.get('href', None)
                    if href_email != None and "@" in href_email:
                        email_string = href_email.replace("\t", "").replace("\n", "").replace(" ", "").replace(
                            "mailto:",
                            "").replace(
                            "?subject=", "").replace("?", "")
                        email = email_string
                        print(url, title, email)
                        self._insert_tuple((url, title, email))


    def _second_level_email_finder(self, url, pattern):
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
            return hrefs_set

        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        second_email_search_filter = soup.find_all(href=re.compile(pattern))

        for pattern_match in second_email_search_filter:
            # Obtained list is inserted in a set for avoiding duplications
            if not pattern_match.attrs.get("data-page-number", False):
                # It will ignore the pagination hrefs
                hrefs_set.add(pattern_match['href'])

        if len(hrefs_set) > 0:
            for link in hrefs_set:
                if ".html" in url:
                    # The final path of the url must be removed
                    url = '/'.join(url.split(".html")[0].split("/")[:-1])
                if not "http" in link:
                    self._fist_level_email_finder(url + link)
                else:
                    self._fist_level_email_finder(link)


    def _paginate_page(self, web_page):
        """
        :param web_page: The web page to try to paginate
        :return: It returns all the possible paginations
        """
        # Html finder
        pagination_urls = set()
        try:
            r = requests.get(web_page)
        except:
            return pagination_urls

        data = r.text
        soup = BeautifulSoup(data, "html.parser")


        for link in soup.find_all(href=re.compile("")):
            if hasattr(link, 'attrs'):
                if link.attrs.get("data-page-number", False):
                    link_goes_to = link.attrs.get("href")
                    if not "http" in link_goes_to:
                        link_goes_to = web_page + link_goes_to
                    pagination_urls.add(link_goes_to)
        return pagination_urls


    def _store_set_in_db(self, emails_set):
        """
        :param emails_set: The elements to store in the database 
        :return: It stores the given set into the given database
        """
        # Create a database connection to a SQLite database and insert the elements
        print("[!] Inserting in DB")
        conn = None
        try:
            conn = sqlite3.connect(self.db_name + ".db")  # Create db connection
            cur = conn.cursor()
            cur.execute(
                " CREATE TABLE IF NOT EXISTS emails(web text, title text, email text, PRIMARY KEY(email))")  # Create emails table
            conn.commit()
            i = 1
            for email in emails_set:
                try:
                    cur.execute("INSERT INTO emails VALUES(?, ?, ?)", (email[0], email[1], email[2]))
                    conn.commit()
                    i += 1
                except:
                    print("{} not inserted due the email is already stored".format(email))

            print("[!] DONE")

        except Error as e:
            print("[X] Error inserting elements in database")
            print(e)
        finally:
            if conn:
                conn.close()


    def find_emails(self):
        """
        :return: It returns a set that contains tuples with information about the found emails. Structure: (url, page tittle, email)
        """
        query_results = self._make_a_google_query(self.query)

        print("[!] Getting the web emails")
        for web_page in query_results:
            try:
                related_pages_to_search = self._paginate_page(web_page)
                related_pages_to_search.add(web_page)
                print("[DEBUG] Going to search in:\n {} ".format(related_pages_to_search))

                for page_to_search in related_pages_to_search:
                    # First level email finder
                    self._fist_level_email_finder(page_to_search)

                    # Second level email finder if it found more links to what I am looking for
                    self._second_level_email_finder(page_to_search, "/Restaurant")
                    self._second_level_email_finder(page_to_search, "/restaurant")

            except:
                pass


    def store_emails(self):
        self.__initialize_db()
        self.find_emails()
        # self._store_set_in_db(self.results_set)

