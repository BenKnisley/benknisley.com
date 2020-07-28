#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 28 July, 2020
"""
import sys
import sqlite3

db_path = "./basic.db"

"""
Database schema

Tables:
    * Posts
        - pageid
        - share/title id
        - title
        - html
"""

def init_database():
    create_auth_table()
    create_pages_table()

def create_pages_table():
    print("Creating Database")
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = """
    CREATE TABLE `pages` (
	`page_id`	TEXT NOT NULL UNIQUE,
	`title_id`	TEXT NOT NULL UNIQUE,
	`title`	TEXT,
	`html`	TEXT,
	PRIMARY KEY(`page_id`));
    """

    ## Setup query arguments
    args = ()
    ## Send query to database
    sql.execute(query, args)

    ## Add changes to database
    conn.commit()

def create_auth_table():
    print("Creating Database")
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = """
    CREATE TABLE `auth_tokens` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `timestamp`	TEXT,
        `hash`	TEXT
    );
    """

    ## Setup query arguments
    args = ()
    ## Send query to database
    sql.execute(query, args)

    ## Add changes to database
    conn.commit()





def add_demo_page():
    print("Adding Demo Page")
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = "INSERT INTO pages VALUES (?, ?, ?, ?)"
    args = ('demodemo', 'demo-page', "Demo Page", "<h1>Hello World</h1><p>Helo World, <br> From Demo Page</p>")

    ## Send query to database
    print( sql.execute(query, args) )

    ## Commit changes to database
    conn.commit()




if __name__ == "__main__":
    if len(sys.argv) > 1:
        command_dict = {
            'create_pages_table':create_pages_table,
            'add_demo_page':add_demo_page,
            'create_auth_table': create_auth_table
            }
        command_dict[sys.argv[1]]()