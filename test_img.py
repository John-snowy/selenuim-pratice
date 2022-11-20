# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 18:03:22 2022

@author: me
"""

import requests
import ddddocr
import YDM_Verify as verify

#header = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36"}
#cookie = [{'domain': '.i.hzmbus.com', 'expiry': 1699864695, 'httpOnly': False, 'name': 'Hm_lvt_ecfd5c356fd652f819555c3c77fd1626', 'path': '/', 'secure': False, 'value': '1668328695'}, {'domain': '.i.hzmbus.com', 'httpOnly': False, 'name': 'Hm_lpvt_ecfd5c356fd652f819555c3c77fd1626', 'path': '/', 'secure': False, 'value': '1668328695'}, {'domain': 'i.hzmbus.com', 'expiry': 1668332294, 'httpOnly': False, 'name': 'acw_sc__v2', 'path': '/', 'secure': False, 'value': '6370acf7ba91682dc1e7efa9c30335f18d3f7c2f'}, {'domain': 'i.hzmbus.com', 'expiry': 1668330494, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': '7819730816683286954135860edaa22005807e2d84b47ebddf7d1a97a3e8a4'}]
#coo = {}
#for v in cookie:
#     print(type(v))
#     coo[v['name']] = v['value']

#print(coo)
#url = "https://i.hzmbus.com/webh5api/captcha?2"
#req = requests.get(url, headers=header, cookies=cookie)
#img_bytes = req.content
#print(req.content)
#ocr = ddddocr.DdddOcr()
#res = ocr.classification(img_bytes)
#print(res)
#req.close()


with open('./response.png', 'rb') as f :
     img_bytes = f.read()

verify_obj = verify.YdmVerify
res = verify_obj.common_verify(verify_obj, img_bytes)
print(res)


