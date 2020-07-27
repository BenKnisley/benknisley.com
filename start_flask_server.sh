#!/bin/bash
## Flask Run File
## Author: Ben Knisley [benknisley@gmail.com]
## Date: March 1, 2020
export FLASK_APP=controller.py
export FLASK_ENV=development

source ./venv/bin/activate
python3 -m flask run
