#!/usr/bin/env python3

import requests

url = 'https://benknisley.com/update_page/index'
post_data = {
    'auth': 'b4pn4zt6pg1oukv2y2cyhe95by6hvv5wvrp2p88cl6y3slnn3f',
    'title': 'Homepage',
    'data': '<h1>Ben Knisley</h1><p>HomePage</p>'
    }
    
files = {
    'profile.jpg': open('/home/ben/Pictures/Profile Pictures/profile.jpg', 'rb')
}

x = requests.post(url, data=post_data, files=files)
print(x.text)
