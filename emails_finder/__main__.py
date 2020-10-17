#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sys utils
import sys

# Email finder

# Excel utils

# Argument parsing
import argparse


TITLE = """
  ______  __  __            _____  _        ______  _____  _   _  _____   ______  _____  
 |  ____||  \/  |    /\    |_   _|| |      |  ____||_   _|| \ | ||  __ \ |  ____||  __ \ 
 | |__   | \  / |   /  \     | |  | |      | |__     | |  |  \| || |  | || |__   | |__) |
 |  __|  | |\/| |  / /\ \    | |  | |      |  __|    | |  | . ` || |  | ||  __|  |  _  / 
 | |____ | |  | | / ____ \  _| |_ | |____  | |      _| |_ | |\  || |__| || |____ | | \ \ 
 |______||_|  |_|/_/    \_\|_____||______| |_|     |_____||_| \_||_____/ |______||_|  \_\ 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
"""


def cli(parser):
    """

    :param parser: The arguments to parse
    :return:       It execute emails_finder with the parsed parameters

    """
    if parser is None:
        raise Exception("[X] ERROR: Parser is None")

    parser = argparse.ArgumentParser(prog='emails_finder', description=TITLE, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-q", "--query", type=str, help="Query to make for your search", required=True)
    parser.add_argument("-d", "--database", type=str, help="Name of the DB to create with the search results")
    parser.add_argument("-e", "--excel", type=str, help="Name of the XLS to create with the search results")

    args = parser.parse_args()

    if not args.database and not args.excel:
        raise Exception("[X] ERROR: Database and/or excel arguments must be included")

    #TODO Execute emails_finder
    elif args.database:
        "generate database"
        if args.excel:
            "generate excel from database"
    elif args.excel:
        "generate excel"

    # Otra opción si finalmente uso la db para generar la excel:
    if args.excel:
        "generate database and excel"
        if args.database:
            "return database y excel"
        else:
            "return excel"

def main():
    try:
        cli(sys.argv[1:])
    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == "__main__":
    print(TITLE)
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\n\tctrl + c detected, exiting...\n')
