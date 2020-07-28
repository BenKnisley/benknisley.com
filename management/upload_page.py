#!/usr/bin/env python3

import requests

url = 'http://127.0.0.1:5000/add_page'
post_data = {
    'title': 'PyMapKit',
    'auth': 'tcc9sqigug4wf5ty3m1ctstjdtvt2r0z6q3m216dco10hb7dei',
    'data': '<h1>It Works</h1><p>Better Homepage Update</p>' 
    }
    
files = {
    'hello.png': open('/home/ben/Development/Resources/image.png', 'rb')
}

x = requests.post(url, data=post_data, files=files)
print(x.text)
