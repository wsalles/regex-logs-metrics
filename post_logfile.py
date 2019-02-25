# -*- coding: utf-8 -*-
import requests

url = 'https://challenge-accept-gcom-stg.herokuapp.com/parse'

for x in range(1, 3):
    file = {'file': open('./logs/log' + str(x) + '.txt', 'rb')}
    result = requests.put(url, files=file)
    print(result.text)