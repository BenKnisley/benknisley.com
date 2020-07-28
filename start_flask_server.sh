#!/bin/bash
## Flask Run File
## Author: Ben Knisley [benknisley@gmail.com]
## Date: March 1, 2020
source ./venv/bin/activate

export FLASK_APP=controller.py
export FLASK_ENV=development
export FLASK_DEBUG=1

python3 -m flask run

