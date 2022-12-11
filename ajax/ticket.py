import os.path

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests


class TicketHelper:
    browser_instance = None

    cookieSavePath = './cache/cookie.json'
    headerSavePath = './cache/header.json'
    userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 holtye'
    urls = {
        "ticket_data_url": "https://i.hzmbus.com/webh5api/manage/query.book.info.data",
        "login_page_url": "https://i.hzmbus.com/webhtml/login",
        # 香港 => 珠海
        "ticket_HKGZHO": "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=香港&xlmc_2=珠海&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO",
    }
    account = {
        "username": 'holtye@qq.com',
        "password": 'yezi0511.'
    }

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
        print(type(cookies_obj))
        if not cookies_obj:
            return False
        for v in cookies_obj:
            self.browser_instance.add_cookie(cookie_dict=v)
        WebDriverWait(self.browser_instance, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sele_date'))
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
            json.loads(content)
        except:
            return False
        else:
            return True

    def get_params_from_cookies_arr(self, arr, key):
        for cookie in arr:
            if key == cookie.__getitem__('name'):
                return cookie.__getitem__('value')

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


if __name__ == '__main__':
    service = TicketHelper()
    login_state = service.check_login()
    if not login_state:
        print('登录状态失效')
        # login_result = service.login()
        # if not login_result:
        #     print('登录失败')
        #     service.browser_instance.quit()
        #     pass
        print('登录成功')
    else:
        print('登录状态依旧有效')
    print('开始自动抢票')

    detail_page_load_status = service.jump_to_ticket_detail()
    resp = service.browser_instance.execute_script("return localStorage.getItem('book_data');")
    print(resp)
