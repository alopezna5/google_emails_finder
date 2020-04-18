#!/usr/bin/env python
# -*- coding: utf-8 -*-

from googlesearch import search
import re
import requests
from bs4 import BeautifulSoup

TITLE = """
  ______  __  __            _____  _        ______  _____  _   _  _____   ______  _____  
 |  ____||  \/  |    /\    |_   _|| |      |  ____||_   _|| \ | ||  __ \ |  ____||  __ \ 
 | |__   | \  / |   /  \     | |  | |      | |__     | |  |  \| || |  | || |__   | |__) |
 |  __|  | |\/| |  / /\ \    | |  | |      |  __|    | |  | . ` || |  | ||  __|  |  _  / 
 | |____ | |  | | / ____ \  _| |_ | |____  | |      _| |_ | |\  || |__| || |____ | | \ \ 
 |______||_|  |_|/_/    \_\|_____||______| |_|     |_____||_| \_||_____/ |______||_|  \_\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
"""

query = "Madrid AND restaurante AND email"

print(TITLE)

print("[!] Making the google query: {} ".format(query))
my_webs_page_result_list = []
for i in search(query,  # The query you want to run
                tld='com',  # The top level domain
                lang='en',  # The language
                num=10,  # Number of results per page
                start=0,  # First result to retrieve
                stop=40,  # Last result to retrieve
                pause=2.0,  # Lapse between HTTP requests
                ):
    my_webs_page_result_list.append(i)
print("[!] DONE")

print("[!] Getting the web emails")
emails_set = set()

for web_page in my_webs_page_result_list:
    try:
        # Html finder
        r = requests.get(web_page)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        # Title finder
        try:
            title = soup.title.text
        except:
            title = None

        # Email finder
        first_email_search_filter = soup.find_all(href=re.compile("mailto"))
        if len(first_email_search_filter) > 1:
            for i in first_email_search_filter:
                if i.string != None and "@" in i.string:
                    i.string = i.string.replace("\t", "").replace("\n", "").replace(" ","")
                    email = i.string
                    emails_set.add((web_page, title, email))
    except:
        pass
print("[!] DONE")

for email in emails_set:
    print(email)
