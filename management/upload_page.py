#!/usr/bin/env python3

import requests

url = 'https://benknisley.com/update_page/index'
post_data = {
    'auth': 'auth_token',
    'title': 'Home',
    'data': '<hr>'
    }
    
files = {
    'profile.jpg': open('/home/ben/Pictures/Profile Pictures/profile.jpg', 'rb')
}

x = requests.post(url, data=post_data, files=files)
print(x.text)
