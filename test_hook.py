import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.chrome.options import Options


def hook():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    prefs = {
        'download.default_directory': os.getenv('./')
    }
    chrome_options.add_experimental_option('prefs', prefs)
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True
    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)

    #设置cdp命令，每次加载页面都会执行改该js内容
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": open('hook.js', encoding='utf-8').read()})

    base_url = 'https://www.baidu.com/'

    driver.get(base_url)
    return driver

    # time.sleep(3)
    # print('第1次获取日志')
    # # 获取日志
    # for entry in driver.get_log('browser'):
    #     print(entry)
    #
    # print('第2次获取日志')
    # # 再次获取日志
    # for entry in driver.get_log('browser'):
    #     print(entry)


# driver.quit()

if __name__ == '__main__':
    hook()
