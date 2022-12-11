from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

#设置日志
d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = {'browser': 'ALL'}

# 启动浏览器
driver = webdriver.Chrome()

#设置cdp命令，每次加载页面都会执行改该js内容
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": open('ajax-hook.js', encoding='utf-8').read()})


base_url = 'https://www.baidu.com/'

driver.get(base_url)

time.sleep(3)
print('第1次获取日志')
#获取日志
for entry in driver.get_log('browser'):
    print(entry)

print('第2次获取日志')
#再次获取日志
for entry in driver.get_log('browser'):
    print(entry)

driver.quit()