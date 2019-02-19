# -*- coding: utf-8 -*-
import requests

url = 'http://localhost/parse'

for x in range(1, 3):
    file = {'file': open('./logs/log' + str(x) + '.txt', 'rb')}
    result = requests.put(url, files=file)
    print(result.text)