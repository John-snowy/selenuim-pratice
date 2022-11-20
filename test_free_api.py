# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:42:59 2022

@author: me
"""

import requests
import base64
import json

str_d="cap.chinaunicom.cn"
with open('./response.png', 'rb') as f :
     img_bytes = f.read()
header = {}
header['Content-Type'] = 'application/json'  
#header['appKey'] = 'fb75eee0-635d-11ed-a699-00163e100db0'
#header['appSecret'] = 'f3c20406aeb9d16234d599d16ca48731'
img = bytes.decode(base64.b64encode(img_bytes))
urlimg = "data:image/png;base64," + img
print(urlimg)
#print(urlimg)
url = 'https://www.345api.cn/api/code/ocr'
#url = 'http://101.201.223.138:9188/api/captcha/simple-captcha'
#url = 'https://china.yescaptcha.com/createTask'
#data = "{\"urlimg\": \"" + urlimg + "\", \"num\": 4, \"type\": \"601\",\"yzmurl\": \"" + url + "\"}"
#data = "{\"clientKey\":\"f08ef032c43408ae60e73ad9901708215342836811822\",\"task\":{\"type\":\"ImageToTextTaskTest\",\"body\":\""+ url +"\"}}"
data = "{\"key\":\"yvBQhgLg6UKI2qXgYsUKfPAqm0\", \"data\":\""+urlimg+"\"}"
#header['Content-Type'] = 'application/json'
r = requests.post(url=url, headers=header, data=data)
print(r.text)
#v_code_json = json.loads(r.text)
#str1 = str(v_code_json['v_code']).lower()
#print(str1)
