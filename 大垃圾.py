# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests

userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 holtye'
urls = {
    "ticket_data_url": "https://i.hzmbus.com/webh5api/manage/query.book.info.data",
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

account = {
    "username": 'holtye@qq.com',
    "password": 'yezi0511.'
}

requiredCookies = {
    "PHPSESSID": "",
    "acw_sc__v2": ""
}
cookieSavePath = './cache/cookie.json'
headerSavePath = './cache/header.json'


def getRequiredCookie():
    # 初始化浏览器
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)
    # 打开页面
    browser.get(urls["login_page_url"])
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'login_box'))
    )
    # 填充内容
    app = browser.find_element(By.ID, 'app')
    box = app.find_element(By.CLASS_NAME, 'login_box')
    form_box = box.find_element(By.CLASS_NAME, 'form_box')
    # 找账号、密码的输入框
    input_list = form_box.find_elements(By.CLASS_NAME, 'input_item')
    # 这里直接输入账号密码
    if len(input_list) > 0:
        inputUser = input_list[0].find_element(By.TAG_NAME, 'input')
        inputPassword = input_list[2].find_element(By.TAG_NAME, 'input')
        inputUser.send_keys(account.get('username'))
        inputPassword.send_keys(account.get('password'))
    # 找登录按钮，并点一下他
    login_btn = form_box.find_element(By.CLASS_NAME, 'login_btn')
    login_btn.click()
    # 等待登录完成
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'action'))
    )
    # 取必要cookie
    phpSessionId = browser.get_cookie('PHPSESSID')
    acwScV2 = browser.get_cookie('acw_sc__v2')
    token = browser.get_cookie('token')
    requiredCookies.__setitem__("PHPSESSID", phpSessionId.get('value'))
    requiredCookies.__setitem__("acw_sc__v2", acwScV2.get('value'))
    # 关闭浏览器
    browser.close()
    # 保存到本地
    saveObjToJsonFile(cookieSavePath, requiredCookies)
    saveObjToJsonFile(headerSavePath, {
        "Authorization": token.get("value"),
    })


def saveObjToJsonFile(filePath, obj):
    with open(filePath, mode='w', encoding='utf-8') as file_obj:
        file_obj.write(json.dumps(obj))
        file_obj.close()


def loadDictFromJsonFile(filePath):
    file_object = open(filePath, 'r')
    str = file_object.read()
    return json.loads(str)


def requestTicketData():
    url = urls.get("ticket_data_url")
    postData = {
        "bookDate": "2022-12-06",
        "lineCode": "HKGZHO",
        "appId": "HZMBWEB_HK",
        "joinType": "WEB",
        "version": "2.7.2032.1262",
        "equipment": "MOBILE"
    }
    # 准备cookie
    cookies_obj = loadDictFromJsonFile(cookieSavePath)
    # 准备header
    headers = loadDictFromJsonFile(headerSavePath)
    headers.__setitem__("User-Agent", userAgent)
    response = requests.post(url, None, postData, headers=headers, cookies=cookies_obj)
    content = response.content
    try:
        res = json.loads(content)
    except:
        print('请求出错，尝试重新登录再试')
        getRequiredCookie()
        requestTicketData()
    else:
        # 如果转换成功了
        print(res)


if __name__ == '__main__':
    # getRequiredCookie()
    requestTicketData()
