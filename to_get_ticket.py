# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 13:55:17 2022

@author: me
"""

from PIL import Image
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import YDM_Verify as verify
import json
import os
import datetime
import calendar
import requests
import time
from selenium.webdriver.chrome.options import Options

import fnmatch
import random

# ua = UserAgent()
header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Mobile Safari/537.36"}
# print(ua.chrome)
urls = {
    "login_page_url": "https://i.hzmbus.com/webhtml/login",
    # 香港 => 澳门
    "ticket_HKGMAC": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=香港&xlmc_2=澳门&xllb=1&xldm=HKGMAC&code_1=HKG&code_2=MAC",
    # 澳门 => 香港
    "ticket_MACHKG": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=澳门&xlmc_2=香港&xllb=1&xldm=MACHKG&code_1=MAC&code_2=HKG",
    # 香港 => 珠海
    "ticket_HKGZHO": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=香港&xlmc_2=珠海&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO",
    # 珠海 => 香港
    "ticket_ZHOHKG": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=珠海&xlmc_2=香港&xllb=1&xldm=ZHOHKG&code_1=ZHO&code_2=HKG",
}

# 这里是需要选择的日期，24并不是24号，选择框里固定是35个日期，需要根据这个月第一天跟最后一天是星期几来判定这个数最终是这个月的哪一天
date_num = 13

cookie_path = "./user0_cookies.txt"
screen_shot_path = './screen_shot.png'
screen_code_path = './screen_code.png'

passenger = "盧育庭"
card_no = "H07508647"

accounts = [
    {
        "account": "2576322300@qq.com",
        "password": "zxcvb110"
    },
    {
        "account": "wurongzhuang@foxmail.com",
        "password": "zxcvb110"
    }
]

linecode = {
    'ZHO2HK': "ZHOHKG",  # 珠海到香港
    "HK2ZHO": "HKGZHO",  # 香港到珠海
    "HK2MAC": "HKGMAC",  # 香港到澳门
    "MAC2HK": "MACHKG"  # 澳门到香港
}


def cal_date():
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    end = calendar.monthrange(year, month)[1]
    start_weekday = calendar.weekday(year, month, 1)
    end_weekday = calendar.weekday(year, month, end)
    return start_weekday


def get_book_date():
    date = time.strftime("%Y-%m", time.localtime())
    print(str(date_num).rjust(2, '0'))
    return date + "-" + str(date_num).rjust(2, '0')

def get_json_file_name():
    files = os.listdir('./')
    files.sort()
    fnames = []
    for f_name in files:
        if fnmatch.fnmatch(f_name, 'price*.json'):
            # print(f_name)
            fnames.append(f_name)
    return fnames[-1]


def ticket_step():
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    prefs = {
        'download.default_directory': 'E:\python乱敲\selenuim'
    }
    chrome_options.add_experimental_option('prefs', prefs)
    # capabilities = webdriver.DesiredCapabilities().CHROME
    # capabilities['acceptSslCerts'] = True
    # browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
    browser = webdriver.Chrome(options=chrome_options)

    #设置cdp命令，每次加载页面都会执行改该js内容
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": open('hook.js', encoding='utf-8').read()})

    # browser = webdriver.Chrome()
    browser.get(urls['ticket_HKGZHO'])
    with open(cookie_path, mode='r', encoding='utf-8') as file_obj:
        cookie = file_obj.read()
    for v in json.loads(cookie):
        #     v['domaion'] = 'i.hzmbus.com'
        browser.add_cookie(cookie_dict=v)
    browser.get(urls['ticket_HKGZHO'])
    browser.refresh()
    print(cookie)
    # browser.navigate().refresh()

    # browser.implicitly_wait(10)
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'sele_date'))
    )
    # 找日期按钮，并换一个
    date_btn = browser.find_element(By.CLASS_NAME, 'sele_date')
    browser.execute_script("arguments[0].click();", date_btn)
    # date_btn.click()
    browser.implicitly_wait(3)

    date_seletor = browser.find_element(By.CLASS_NAME, 'date_alert')
    date_list = date_seletor.find_elements(By.CLASS_NAME, 'wh_content')
    print(len(date_list))
    if len(date_list) > 0:
        date_btns = date_list[1].find_elements(By.CLASS_NAME, 'wh_content_item')
        print(len(date_btns))
        if len(date_btns) > 0:
            first_weekday = cal_date()
            browser.execute_script("arguments[0].click();", date_btns[date_num + first_weekday - 1])
            # date_btns[22].click()
            print('我选了日期了')

    # 找日间、夜间按钮
    day_btn = browser.find_element(By.CLASS_NAME, 'day')
    night_btn = browser.find_element(By.CLASS_NAME, 'night')

    # 找预约票按钮
    book_btn = browser.find_element(By.CLASS_NAME, 'bookRight')
    sel_btn = book_btn.find_element(By.CLASS_NAME, 'seleIcon')
    browser.execute_script("arguments[0].click();", sel_btn)
    # sel_btn.click()

    # 这里预留要选预约时间

    # 找姓名、身份证输入框
    # 姓名输入框
    name_inp_box = browser.find_element(By.CLASS_NAME, 'up')
    name_inp_div = name_inp_box.find_element(By.CLASS_NAME, 'input')
    name_inp = name_inp_div.find_element(By.TAG_NAME, 'input')
    name_inp.send_keys(passenger)

    # 身份证输入框
    card_no_inp_box = browser.find_element(By.CLASS_NAME, 'down')
    card_no_inp_div = card_no_inp_box.find_element(By.CLASS_NAME, 'input')
    card_no_inp = card_no_inp_div.find_element(By.TAG_NAME, 'input')
    card_no_inp.send_keys(card_no)

    # js="var q=document.documentElement.scrollTop=10000"
    # js = "var q=document.body.scrollTop=10000"

    # browser.execute_script(js)
    # browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # 验证码处理
    captcha_box = browser.find_element(By.CLASS_NAME, 'captchaBox')
    captcha_img = captcha_box.find_element(By.TAG_NAME, 'img')
    captcha_inp = captcha_box.find_element(By.TAG_NAME, 'input')
    # captcha_url = captcha_img.get_attribute('src')
    location = captcha_img.location
    size = captcha_img.size

    # 滑到浏览器最底部，并进行截图处理
    browser.execute_script("arguments[0].scrollIntoView();", captcha_img)

    browser.save_screenshot(screen_shot_path)
    # print(captcha_url)
    # print(location)
    # print(size)

    # 做验证码的识别（调api要花钱，先注释掉）
    res = code_verify()
    captcha_inp.send_keys(res)

    # 登录按钮
    agree_box = browser.find_element(By.CLASS_NAME, 'hint')
    agree_btn = agree_box.find_element(By.TAG_NAME, 'span')
    # agree_btn.click()
    browser.execute_script("arguments[0].click();", agree_btn)

    os.system("pause")
    # pay_btn = browser.find_element(By.CLASS_NAME, 'bottom')
    # pay_btn.click()

    # print(browser.page_source)
    # browser.close()


def code_verify():
    # 这里是固定了用浏览器打开页面验证码的位置
    left = 730
    top = 700
    right = 865
    bottom = 745

    # 通过Image处理图像
    im = Image.open(screen_shot_path)
    im = im.crop((left, top, right, bottom))
    im.save(screen_code_path)

    # ocr = ddddocr.DdddOcr()
    with open(screen_code_path, 'rb') as f:
        img_bytes = f.read()
    # captcha_img.click()

    verify_obj = verify.YdmVerify
    # res = ocr.classification(img_bytes)
    # print(res)
    # if len(res) < 1:
    res = verify_obj.common_verify(verify_obj, img_bytes)
    print("api的结果:" + res)
    return res


def craw_post(rdm):
    cookie_chooese = './user' + str(rdm) + '_cookies.txt'

    cookies = {}
    with open(cookie_chooese, mode='r', encoding='utf-8') as file_obj:
        cookie = file_obj.read()
    for v in json.loads(cookie):
        cookies[v['name']] = v['value']
    url = "https://i.hzmbus.com/webh5api/manage/query.book.info.data"

    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJla2p0X2lzcyIsImlhdCI6MTY3MDE0MDUyNSwiZXhwIjoxNjcwMTQ3NzI1LCJhdWQiOiJla2p0X2NsaWVudF9hdWQiLCJzdWIiOiJla2p0X2NsaWVudF9zdWIiLCJuYmYiOjE2NzAxNDA1MjUsImp0aSI6ImVranRfanRpXzE2NzAxNDA1MjUiLCJkYXRhIjoic1pIV1REbzFDNm8wam1vR2JBQ1ZXU3RQU25ocVQrM2N6d3UyK2MrZXNmMnhiOGhPUkh0SEFxQzBhN0RUS082WjdxQnFTbktRZ3dCR0tcL2JFMHV4dTJjMzdKUkZDb2FXUHQxcEZvV0xZQmRLdWdwdGEyWmdMT0ZVa3dzWFwvTEl1VzJ6RzRkVElXWmJhZHdUXC84TElUQzR5cWw0YVplZ0NIekc2bGdOcXFqZFdlTExaNVBvZGw1SlkxTm1UUlVZaTAzVTVheHZVUlBsR1NNNllTOHl5U1wvWnFYSFlKNk1MZUhvcTF5UjNLOGJCSWFNTEJoZzd3VzlPYkJpcWNEWlg1ZjRuc3U1VWRMZ1p4NVBKRkhFczhIXC9aUGowYithamJ0TkRnOVRcLzc4N0pnTlMwU0l5eUUzdHpuVVVMd3ZpZFNBNThGZ2YwWjV4Ukt3Ym1TQkl5Q3M5eGZwTGVEMTNEXC9ZSnNcL05TcGlzUU5uV2N0K1d6K096T0xVcHlteVpLZU52MWxtbVUyOTFVVkdrQklcL1BNditwbmxMdTEwMm1aeEowbVhQZDFqUUpsVDdQWnd6T3VCNHp4QjFrTHNKd05wdlNIU013eldWYjhrQ1FQcERQYnpHY250MWVuVUVYZ3JDTzFWVEswb2RQN0xxVlwvNDBcL3hlYWRRdUN5a1NOemZLYkwyTGNrUWJBNE1XaEozZ1RQa0MyZGFNdmMydHdoNjdSMkZrMEEyUlVyTnN6dlZkODFkY0h5S0lyeWQrTnRwQUZoeEJ0MWpvUm1SZ2JiXC93V3RwRkdaQlZyTElRUWQ2R3RKZUptQ3VDRWRmdmF2ZWk3UGpBVE9QaTA2dVZoVDNaMHZcL1ZsMHF1N05TOXlFYllrN3F5VURSQ1wva3Jiako2a1pmTUpMdnJ4VythXC9GS3dpb2hNQWpPcDVtbnFHbktmWnNSTXlHdm9JSklsNUtEelFwU0M4SjMyZUZpTXZ2WU5FMmNmaU9vdGhDOG5pdjgwamcxK09uT2JaXC9wWkIrVW1YS2V3akhcL1JzclpVNWpuRHVVdXRjV091ckhGZ2ZjMGFcLzRQb21Gamk3WElMZEdpTE84eDZaSTd3SlpaZTZwbTBlSkxFaTlkSm14U3ZCUkM5QzJHMStjN3J6THo5TkVMSFhGK0VhMGpIbTh6MjA1d3JuVElJaWdjTWZTNVJQMmdSczFjVFVYczZoS2EwcTU1a0gxU1Jhb2picHN0V2pUck1uVXpGc2FBeXczZVRlcW83elVQUEpFeEVycDhGYlwvb2I0SVRWOXVFQ0E0UzBLcEY4a29ZTUNUVmRDZU9qWVZWS3FvV1pvdGM0eldEdDJVdVZcL2VESGQ5c3FcL1Q0ajQ4d0QycjgydSJ9.1f-EZcjq_uskJTsGBxW3W8EgIgmvZ0ulQlLi-KNyV9k",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
        "sec-ch-ua-platform": "Windows",
        "Origin": "https://i.hzmbus.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "i.hzmbus.com",
        "Accept-Encoding": "gzip, deflate, br"
    }
    data = {
        "appId": "HZMBWEB_HK",
        "bookDate": get_book_date(),
        "equipment": "PC",
        "joinType": "WEB",
        "lineCode": "MACHKG",
        "version": "2.7.2032.1262"
    }
    print(cookies)

    response = requests.request("POST", url, headers=headers, data=json.dumps(data), cookies=cookies)
    print("cookies:")
    print(response.cookies)
    print("headers:")
    print(response.headers)

    try:
        rsp = json.loads(response.text)
        print(rsp)
        if "responseData" in rsp:
            print("responseData 在返回体里面")
            print(rsp['responseData'])
            for v in rsp['responseData']:
                if "maxPeople" in v:
                    print(v['maxPeople'])
                    if v['maxPeople'] > 0:
                        return True
    except:
        print("没啥就是返回的接口体有毛病:" + response.text)
    return False


if __name__ == '__main__':

    # file = get_json_file_name()
    # print(file)
    ticket_step()
    # os.system("pause")

    pass
