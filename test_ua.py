from fake_useragent import UserAgent
import os
import random
import json

if __name__ == '__main__':
    # print(fake_useragent.VERSION)
    # location = os.getcwd() + '\\fake_useragent.json'
    # ua = UserAgent(verify_ssl=False, cache=False, use_cache_server=False, path=location)
    # print(ua.chrome)
    #
    # print(ua.path)
    rdm = random.randint(0, 1)
    cookies = {}
    cookie_chooese = './user'+str(rdm)+'_cookies.txt'
    with open(cookie_chooese, mode='r', encoding='utf-8') as file_obj:
        cookie = file_obj.read()
    for v in json.loads(cookie):
        cookies[v['name']] = v['value']
    print(cookies.keys())
    print(cookies.values())

