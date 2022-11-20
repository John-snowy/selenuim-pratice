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
import ddddocr
import json
import os
import datetime
import calendar

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
date_num = 24

cookie_path = "./cookie.txt"
screen_shot_path = './screen_shot.png'
screen_code_path = './screen_code.png'

account = "2576322300@qq.com"
password = "zxcvb110"

passenger = "吴讲德"
card_no = "445242324234234234234"

def cal_date():
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    end = calendar.monthrange(year, month)[1]
    start_weekday = calendar.weekday(year, month, 1)
    end_weekday = calendar.weekday(year, month, end)
    return start_weekday

def login_step():
    # 这里打开登录页面
    browser = webdriver.Chrome()
    # browser.maximize_window()
    browser.get(urls["login_page_url"])
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'login_box'))
    )
    # browser.implicitly_wait(5) #设置等待20秒钟
    # cookie = browser.get_cookies()
    app = browser.find_element(By.ID, 'app')
    box = app.find_element(By.CLASS_NAME, 'login_box')
    form_box = box.find_element(By.CLASS_NAME, 'form_box')
    # 找账号、密码的输入框
    input_list = form_box.find_elements(By.CLASS_NAME, 'input_item')
    # print(cookie)
    # print(len(inputList))
    # 这里直接输入账号密码
    if len(input_list) > 0:
        inputUser = input_list[0].find_element(By.TAG_NAME, 'input')
        inputPassword = input_list[2].find_element(By.TAG_NAME, 'input')
        inputUser.send_keys(account)
        inputPassword.send_keys(password)
    # 找登录按钮，并点一下他
    login_btn = form_box.find_element(By.CLASS_NAME, 'login_btn')
    login_btn.click()
    # 等渲染跳转的首页页面
    # browser.implicitly_wait(10)
    # time.sleep(20)
    # 显示等待登录后页面跳转
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'action'))
    )

    # 先不要了 start
    # 随便点击一个框进入
    # action_box = browser.find_element(By.CLASS_NAME,'box')
    # btns = action_box.find_elements(By.TAG_NAME, 'td')
    # btns[0]  香港 => 珠海
    # btns[1]  珠海 => 香港
    # btns[2]  香港 => 澳门
    # btns[3]  澳门 => 香港
    # print(browser)
    # print(action_box)
    # print(len(btns))
    # print(btns)
    # if len(btns) > 0:
    #     btns[0].click()
    # else:
    #     print("页面没渲染好，找不到可以按的地方")

    # 先不要了 end

    # 登录跳转首页
    cookie = browser.get_cookies()
    browser.close()
    with open(cookie_path, mode='w', encoding='utf-8') as file_obj:
        file_obj.write(json.dumps(cookie))
    print(cookie)

def ticket_step():
    browser = webdriver.Chrome()
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
            browser.execute_script("arguments[0].click();", date_btns[date_num+first_weekday-1])
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

    #滑到浏览器最底部，并进行截图处理
    browser.execute_script("arguments[0].scrollIntoView();", captcha_img)

    browser.save_screenshot(screen_shot_path)
    # print(captcha_url)
    #print(location)
    #print(size)

    #做验证码的识别（调api要花钱，先注释掉）
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

    #ocr = ddddocr.DdddOcr()
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

if __name__ == '__main__':
    ticket_step()
    os.system("pause")
