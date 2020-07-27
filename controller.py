#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Date: 27 July, 2020
"""
from flask import Flask
app = Flask(__name__, static_folder="static")


@app.route('/')
def index():
    return "Hello World"


Envirment