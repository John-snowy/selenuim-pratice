from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

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

cookie_path = "./cookie.txt"

account = "2576322300@qq.com"
password = "zxcvb110"

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


if __name__ == '__main__':
    login_step()