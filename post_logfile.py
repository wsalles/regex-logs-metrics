# -*- coding: utf-8 -*-
import requests

url = 'http://localhost/parse'

file = {'file': open('log2.txt', 'rb')}

result = requests.post(url, files=file)

print(result.text)