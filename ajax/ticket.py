import calendar
import datetime
import os.path
import time
import os
import re
import base64

from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import argparse
import requests
import YDM_Verify as verify


def cal_date():
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    end = calendar.monthrange(year, month)[1]
    start_weekday = calendar.weekday(year, month, 1)
    end_weekday = calendar.weekday(year, month, end)
    return start_weekday


class TicketHelper:
    passengers = [
        # {"name": "王玉环", "id": "H01406348"},
        # {"name": "刘启", "id": "H08111297"},
    ]

    def __init__(self, username, password, date_num, date_num_list, passenger, card_no):
        self.account = {
            "username": username,
            "password": password,
        }
        self.date_num_wanted = int(date_num)
        self.date_num = int(date_num)
        self.date_num_list = ''
        if not (date_num_list is None):
            self.date_num_list = date_num_list.split(',')
        self.date_num_len = len(self.date_num_list)
        self.date_num_try = 0
        self.passenger = passenger
        self.card_no = card_no
        self.browser_instance = None
        self.screenShotPath = './screen_shot.png'
        self.screenCodePath = './captcha.png'
        self.cookieSavePath = './cache/cookie.json'
        self.headerSavePath = './cache/header.json'
        self.userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 holtye'
        self.urls = {
            "ticket_data_url": "https://i.hzmbus.com/webh5api/manage/query.book.info.data",
            "login_page_url": "https://i.hzmbus.com/webhtml/login",
            # 香港 => 珠海
            "ticket_HKGZHO": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=香港&xlmc_2=珠海&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO",
            # 香港 => 澳门
            "ticket_HKGMAC": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=香港&xlmc_2=澳门&xllb=1&xldm=HKGMAC&code_1=HKG&code_2=MAC",
            # 澳门 => 香港
            "ticket_MACHKG": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=澳门&xlmc_2=香港&xllb=1&xldm=MACHKG&code_1=MAC&code_2=HKG",
            # 珠海 => 香港
            "ticket_ZHOHKG": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=珠海&xlmc_2=香港&xllb=1&xldm=ZHOHKG&code_1=ZHO&code_2=HKG",
        }
        # 跟日期 挂钩，如果是true就往后一天买票，如果false就往前一天买票
        self.flag = True

    def init_browser(self):
        # 设置日志
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = {'browser': 'ALL'}
        # 初始化浏览器
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.browser_instance = webdriver.Chrome(options=options)

    def hook(self):
        # 获取日志
        for entry in self.browser_instance.get_log('browser'):
            print(entry)

    def to_new_page(self, url):
        self.init_browser()
        self.browser_instance.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                                              {"source": open('ajax-hook.js', encoding='utf-8').read()})
        self.browser_instance.get(url)

    def login(self):
        self.to_new_page(self.urls["login_page_url"])
        WebDriverWait(self.browser_instance, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'login_box'))
        )
        # 填充内容
        app = self.browser_instance.find_element(By.ID, 'app')
        box = app.find_element(By.CLASS_NAME, 'login_box')
        form_box = box.find_element(By.CLASS_NAME, 'form_box')
        # 找账号、密码的输入框
        input_list = form_box.find_elements(By.CLASS_NAME, 'input_item')
        # 这里直接输入账号密码
        if len(input_list) > 0:
            account_input_dom = input_list[0].find_element(By.TAG_NAME, 'input')
            password_input_dom = input_list[2].find_element(By.TAG_NAME, 'input')
            account_input_dom.send_keys(self.account.get('username'))
            password_input_dom.send_keys(self.account.get('password'))
        # 找登录按钮，并点一下他
        login_btn = form_box.find_element(By.CLASS_NAME, 'login_btn')
        login_btn.click()
        # 等待登录完成
        WebDriverWait(self.browser_instance, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'action'))
        )
        cookie = self.browser_instance.get_cookies()
        self.save_obj_to_json_file(self.cookieSavePath, cookie)
        self.browser_instance.quit()
        return True

    def jump_to_ticket_detail(self):
        self.to_new_page(self.urls['ticket_HKGZHO'])
        # 准备cookie
        cookies_obj = self.load_dict_from_json_file(self.cookieSavePath)
        if not cookies_obj:
            return False
        for v in cookies_obj:
            self.browser_instance.add_cookie(cookie_dict=v)

        self.browser_instance.get(self.urls['ticket_HKGZHO'])
        WebDriverWait(self.browser_instance, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'captchaBox'))
        )
        return True

    def check_login(self):
        url = self.urls.get("ticket_data_url")
        postData = {
            "bookDate": "2022-12-06",
            "lineCode": "HKGZHO",
            "appId": "HZMBWEB_HK",
            "joinType": "WEB",
            "version": "2.7.2032.1262",
            "equipment": "MOBILE"
        }
        # 准备cookie
        cookies_obj = self.load_dict_from_json_file(self.cookieSavePath)
        if not cookies_obj:
            return False
        try:
            headers = {
                "User-Agent": self.userAgent,
                "Authorization": self.get_params_from_cookies_arr(cookies_obj, 'token')
            }
            cookies = {
                "PHPSESSID": self.get_params_from_cookies_arr(cookies_obj, 'PHPSESSID'),
                "acw_sc__v2": self.get_params_from_cookies_arr(cookies_obj, 'acw_sc__v2')
            }
            response = requests.post(url, None, postData, headers=headers, cookies=cookies)
            content = response.content
            data = json.loads(content)
            print(data)
            if data['code'] != 'SUCCESS':
                return False
        except:
            return False
        else:
            return True

    def get_params_from_cookies_arr(self, arr, key):
        for cookie in arr:
            if key == cookie.__getitem__('name'):
                return cookie.__getitem__('value')

    def ticket_page_auto_filter(self):
        # 自动换下日期
        login_status = self.auto_switch_date()
        if not login_status:
            return False

        # 找日间、夜间按钮
        day_btn = self.browser_instance.find_element(By.CLASS_NAME, 'day')
        night_btn = self.browser_instance.find_element(By.CLASS_NAME, 'night')

        # 找预约票按钮
        book_btn = self.browser_instance.find_element(By.CLASS_NAME, 'bookRight')
        sel_btn = book_btn.find_element(By.CLASS_NAME, 'seleIcon')
        self.browser_instance.execute_script("arguments[0].click();", sel_btn)

        # 这里预留要选预约时间

        # 找姓名、身份证输入框
        if len(self.passengers) > 1:
            clickNum = len(self.passengers) - 1
            addBtn = self.browser_instance.find_element(By.CLASS_NAME, 'add')
            for num in range(0, clickNum):
                self.browser_instance.execute_script("arguments[0].click();", addBtn)
            name_inp_box = self.browser_instance.find_elements(By.CLASS_NAME, 'up')
            card_no_inp_box = self.browser_instance.find_elements(By.CLASS_NAME, 'down')
            for num in range(0, len(self.passengers)):
                # 姓名
                name_inp_div = name_inp_box[num].find_element(By.CLASS_NAME, 'input')
                name_inp = name_inp_div.find_element(By.TAG_NAME, 'input')
                name_inp.send_keys(self.passengers[num]['name'])
                # id
                card_no_inp_div = card_no_inp_box[num].find_element(By.CLASS_NAME, 'input')
                card_no_inp = card_no_inp_div.find_element(By.TAG_NAME, 'input')
                card_no_inp.send_keys(self.passengers[num]['id'])
        else:
            # 姓名输入框
            name_inp_box = self.browser_instance.find_element(By.CLASS_NAME, 'up')
            name_inp_div = name_inp_box.find_element(By.CLASS_NAME, 'input')
            name_inp = name_inp_div.find_element(By.TAG_NAME, 'input')
            name_inp.send_keys(self.passenger)
            # 身份证输入框
            card_no_inp_box = self.browser_instance.find_element(By.CLASS_NAME, 'down')
            card_no_inp_div = card_no_inp_box.find_element(By.CLASS_NAME, 'input')
            card_no_inp = card_no_inp_div.find_element(By.TAG_NAME, 'input')
            card_no_inp.send_keys(self.card_no)

        # 验证码处理
        captcha_box = self.browser_instance.find_element(By.CLASS_NAME, 'captchaBox')
        captcha_img = captcha_box.find_element(By.TAG_NAME, 'img')
        js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
             "let img = document.getElementsByTagName('img')[0]; /*找到图片*/ " \
             "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
             "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
             "let base64String = c.toDataURL();return base64String;"

        base64_str = self.browser_instance.execute_script(js)
        img = self.base64_to_image(base64_str)

        img.save('captcha.png')

        captcha_inp = captcha_box.find_element(By.TAG_NAME, 'input')

        # 做验证码的识别（调api要花钱，先注释掉）
        # res = self.code_verify()
        # captcha_inp.send_keys(res)
        # 滑到浏览器最底部，并进行截图处理

        # 登录按钮
        agree_box = self.browser_instance.find_element(By.CLASS_NAME, 'hint')
        agree_btn = agree_box.find_element(By.TAG_NAME, 'span')
        # agree_btn.click()
        self.browser_instance.execute_script("arguments[0].click();", agree_btn)

        # pay_btn = self.browser_instance.find_element(By.CLASS_NAME, 'bottom')
        # pay_btn.click()

        # print(self.browser_instance.page_source)
        # self.browser_instance.close()
        return True

    @staticmethod
    def base64_to_image(base64_str):
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        return img

    def select_date(self):
        # 找日期按钮，并换一个
        date_btn = self.browser_instance.find_element(By.CLASS_NAME, 'sele_date')
        self.browser_instance.execute_script("arguments[0].click();", date_btn)
        self.browser_instance.implicitly_wait(3)

        date_seletor = self.browser_instance.find_element(By.CLASS_NAME, 'date_alert')
        date_list = date_seletor.find_elements(By.CLASS_NAME, 'wh_content')
        if len(date_list) > 0:
            date_btns = date_list[1].find_elements(By.CLASS_NAME, 'wh_content_item')
            if len(date_btns) > 0:
                first_weekday = cal_date()
                self.browser_instance.execute_script("arguments[0].click();",
                                                     date_btns[self.date_num + first_weekday - 1])
                print('我选了日期:' + str(self.date_num))

    def auto_switch_date(self):
        self.select_date()

        while True:
            while True:
                book_stat = service.browser_instance.execute_script("return localStorage.getItem('book_stat');")
                if int(book_stat) == 1:
                    break
            # 选好日期之后，判断下还有没有票剩余
            resp = service.browser_instance.execute_script("return localStorage.getItem('book_data');")
            print(resp)
            try:
                resp = json.loads(resp)
                print(resp)
                # 这一步校验下是否登录态失效了
                if resp['code'] != 'SUCCESS':
                    print('切换日期登录状态失效')
                    service.browser_instance.quit()
                    return False
                if resp['responseData'][0]['maxPeople'] == 0:
                    self.choose_date_num()
                    time.sleep(5)
                    self.select_date()
                else:
                    break
            except:
                print("从localstorage里面获取的数据有问题，json转换报错了")
                continue
        return True

    def choose_date_num(self):
        if self.date_num_len > 0:
            self.date_num = int(self.date_num_list[self.date_num_try % self.date_num_len])
            self.date_num_try += 1
        else:
            if self.flag:
                self.flag = False
                self.date_num = self.date_num_wanted + 1
            else:
                self.flag = True
                self.date_num = self.date_num_wanted - 1

    def code_verify(self):
        # ocr = ddddocr.DdddOcr()
        with open(self.screenCodePath, 'rb') as f:
            img_bytes = f.read()

        verify_obj = verify.YdmVerify
        res = verify_obj.common_verify(verify_obj, img_bytes)
        print("api的结果:" + res)
        return res

    @staticmethod
    def save_obj_to_json_file(filePath, obj):
        with open(filePath, mode='w', encoding='utf-8') as file_obj:
            file_obj.write(json.dumps(obj))
            file_obj.close()

    @staticmethod
    def load_dict_from_json_file(filePath):
        if not os.path.exists(filePath):
            return False
        file_object = open(filePath, 'r')
        str = file_object.read()
        return json.loads(str)


parser = argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('-username', '-u', help='登录账号', default='holtye@qq.com')
parser.add_argument('-password', '-pw', help='登录账号对应的密码', default='yezi0511')
parser.add_argument('-date_num', '-dn', help='买票日期', required=True)
parser.add_argument('-date_num_list', '-dnl', help='买票日期区间')
parser.add_argument('-passenger', '-pa', help='乘车人名字', required=True)
parser.add_argument('-card_no', '-cn', help='乘车人身份证', required=True)
args = parser.parse_args()

if __name__ == '__main__':
    service = TicketHelper(args.username, args.password, args.date_num, args.date_num_list, args.passenger,
                           args.card_no)
    while True:
        login_state = service.check_login()
        if not login_state:
            print('登录状态失效')
            login_result = service.login()
            if not login_result:
                print('登录失败')
                service.browser_instance.quit()
                break
            print('登录成功')
        else:
            print('登录状态依旧有效')
        print('开始自动抢票')

        detail_page_load_status = service.jump_to_ticket_detail()
        check_login = service.ticket_page_auto_filter()
        if check_login:
            break
