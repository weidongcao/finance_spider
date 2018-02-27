"""
Selenium是一个自动化测试工具，利用它我们可以驱动渡口执行特定的动作，
如点击、下拉等等操作，同时还可以获取浏览器当前呈现的页面的源代码，做到
可见即可爬。对于一些JavaScript动态渲染的页面来说，此种抓取方式非常有效，
本节让我们来感受一下它的强大之处吧
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()

browser = webdriver.Chrome()
browser.get('https://www.jin10.com')
input_first = browser.find_element_by_id('J_flashMoreBtn')
input_second = browser.find_element_by_css_selector('#J_flashMoreBtn')
input_third  = browser.find_element_by_xpath('//*[@id="J_flashMoreBtn"]')
print(input_first, input_second, input_third)

browser.close()
