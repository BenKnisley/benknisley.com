#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 28 July, 2020
"""
import sys
import sqlite3
import time
import random
import hashlib, binascii

db_path = "./database.db"

def init_database():
    create_auth_table()
    create_pages_table()
    print(generate_auth_token())
    print("Don't forget to run 'chown www-data:www-data ./database.db' and chmod 0777 ./database.db")

def create_pages_table():
    print("Creating Database")
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = """
    CREATE TABLE `pages` (
	`page_id`	TEXT NOT NULL UNIQUE,
	`title_id`	TEXT NOT NULL UNIQUE,
    `timestamp`	INTEGER,
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

    ## Setup add query
    query = "INSERT INTO pages VALUES (?, ?, ?, ?, ?)"

    ## Add home placeholder
    args = ('index', 'index', 0, 'Home', '<hr>')
    sql.execute(query, args)

    ## Add resume placeholder
    args = ('resume', 'resume', 0, 'Resume', '<hr>')
    sql.execute(query, args)

    ## Commit changes to database
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

def delete_page(title_id):
    print(f"deleting {title_id}")
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = "DELETE FROM pages WHERE title_id = ?;"

    ## Setup query arguments
    args = (title_id)

    ## Send query to database
    sql.execute(query, args)

    ## Add changes to database
    conn.commit()

##
def generate_auth_token():
    id_length = 50
    chars = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    ## Get one random char, can't be digit

    ## Create rest of string
    new_token = ''.join(random.choice(chars + digits) for _ in range(id_length))

    ## Generate hash
    hash_code = hashlib.pbkdf2_hmac('sha256', bytes(new_token, 'utf-8'), b'saltwater', 500000)
    hash_code = str(binascii.hexlify(hash_code), 'utf-8')

    ## Create database connection and cursor
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()
    
    ## Setup query
    query = "INSERT INTO auth_tokens VALUES (NULL, ?, ?)"
    args = (int(time.time()), hash_code)

    ## Send query to database, and commit
    sql.execute(query, args)
    conn.commit()

    ## Return new_token
    return new_token


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command_dict = {
            'init_database': init_database,
            'generate_auth_token': generate_auth_token,
            'create_pages_table':create_pages_table,
            'add_demo_page':add_demo_page,
            'create_auth_table': create_auth_table,
            'delete_page': delete_page
            }
        
        if sys.argv[2:]:
            print( command_dict[sys.argv[1]](sys.argv[2:]))
        else:
            print( command_dict[sys.argv[1]]())
    else: 
        print("Commands:")
        print("============================")
        print('db_manager.py init_database')
        print('db_manager.py generate_auth_token')
        print('db_manager.py create_pages_table')
        print('db_manager.py add_demo_page')
        print('db_manager.py create_auth_table')
        print('db_manager.py delete_page <page_id>')