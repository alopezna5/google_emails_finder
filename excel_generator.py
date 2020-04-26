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

from xlsxwriter.workbook import Workbook

try:
    # Create the sheet
    workbook = Workbook('emails_database_tres_cantos.xlsx')
    worksheet = workbook.add_worksheet()

    # Read all the database content
    conn = sqlite3.connect("emails_database_tres_cantos.db")  # Create db connection
    cur = conn.cursor()
    all_emails_info = cur.execute("select * from emails")

    # Store the read information
    for i, row in enumerate(all_emails_info):
        for j, value_to_insert in enumerate(row):
            worksheet.write(i, j, value_to_insert)

except Error as e:
    print("[X] Error inserting elements in database")
    print(e)

finally:
    if conn:
        conn.close()
    if workbook:
        workbook.close()

