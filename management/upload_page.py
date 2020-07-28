#!/usr/bin/env python3


with open('./management/auth_token.txt', 'r') as f:
    auth_token = f.read()

import requests

url = 'https://benknisley.com/update_page/index'
post_data = {
    'auth': auth_token,
    'title': 'Home',
    'data': """
    <img src="profile.jpg" width="125" class="left">
    <br>
    <h1>Ben Knisley</h1>
    <p>GIS Analyst at Crown Castle</p>
    <p>Python programmer & cartographer</p>
    <br>
    <hr class="dashed" >
    """
    }
    
files = {
#    'profile.jpg': open('/home/ben/Pictures/Profile Pictures/profile.jpg', 'rb')
}

x = requests.post(url, data=post_data, files=files)
print(x.text)
