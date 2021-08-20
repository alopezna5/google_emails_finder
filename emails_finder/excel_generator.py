#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Database utils
import sqlite3
from sqlite3 import Error

from xlsxwriter.workbook import Workbook


class excel_utils():


    def generate_excel_from_sqlite3_db(self, sqlite_path, resultant_excel_name):
        """
        :param sqlite_path: Path to the sqlite DB
        :return: At the moment this method is only working for generated DB by email_finder. It generates a emails excel
        """

        try:
            # Create the sheet
            workbook = Workbook(resultant_excel_name)
            worksheet = workbook.add_worksheet()

            # Read all the database content
            conn = sqlite3.connect(sqlite_path)  # Create db connection
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

