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
import datetime

db_path = "/var/www/benknisley.com/database.db"

def generate_pageid():
    """
    Generates a pageID
    """
    ## Create pool of chars and numbers to select from, abd lenght of ID
    id_length = 7
    chars = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    ## Create rest of string
    new_id = ''.join(random.choice(chars + digits) for _ in range(id_length))
    
    return new_id

def generate_title_id(title):
    """ """
    ## Remove bordering whitespace
    title_id = title.strip()

    ## Make all chars lowercase
    title_id = title_id.lower()

    ## Replace lines with dashes
    title_id = title_id.replace(' ', '-')

    ## Return cleaned title_id
    return title_id

def add_page(title, html):
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    page_id = generate_pageid()
    title_id = generate_title_id(title)
    timestamp = int(time.time())

    ## Setup query
    query = "INSERT INTO pages VALUES (?, ?, ?, ?, ?)"
    args = (page_id, title_id, timestamp, title, html)

    ## Send query to database
    sql.execute(query, args)

    ## Commit changes to database
    conn.commit()

    return page_id

def update_page(page_id, title, html):
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    title_id = generate_title_id(title)

    ## Setup query
    query = """
        UPDATE pages
        SET title_id = ?, title = ?, html = ?
        WHERE page_id = ?; 
    """
    args = (title_id, title, html, page_id)

    ## Send query to database
    sql.execute(query, args)

    ## Commit changes to database
    conn.commit()

def get_page(id):
    ## Create database connection and cursor
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = "SELECT title, html FROM pages WHERE page_id=? OR title_id=?;"
    args = (id, id,)

    ## execute query on database
    sql.execute(query, args)

    ## Get and return data from query
    return sql.fetchone()

def get_posts():
    ## Create database connection and cursor
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()

    ## Setup query
    query = "SELECT page_id, title, timestamp FROM pages;"
    args = ()

    ## execute query on database
    sql.execute(query, args)
    
    pages = sql.fetchall()
    posts = []

    for page in pages:
        ## Uppack page
        page_id, title, timestamp = page
        
        ## Skip index and resume
        if page_id in ('index', 'resume'):
            continue

        ## Create a list to store post data
        post = []

        ## Add page_id, and title
        post.append(page[0])
        post.append(page[1])

        ## Add a human timestamp
        timestr = f"{datetime.datetime.fromtimestamp(page[2]):%d %b, %Y}"
        post.append(timestr)

        ## Add post data to posts list
        posts.append(post)

    ## Get and return data from query
    return posts


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

def check_token(token):
    ## Generate hash
    hash_code = hashlib.pbkdf2_hmac('sha256', bytes(token, 'utf-8'), b'saltwater', 500000)
    hash_code = str(binascii.hexlify(hash_code), 'utf-8')

    ## Create database connection and cursor
    conn = sqlite3.connect(db_path)
    sql = conn.cursor()
    
    ## Setup query
    query = "SELECT id FROM auth_tokens WHERE hash=?;"
    args = (hash_code,)

    ## Send query to database
    sql.execute(query, args)

    hash_id = sql.fetchone()

    if hash_id == None:
        return False
    else:
        return True