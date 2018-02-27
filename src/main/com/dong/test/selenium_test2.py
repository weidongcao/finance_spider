"""
测试Selenium调用谷歌浏览器爬取数据
"""
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.jin10.com')
input_first = browser.find_element_by_id('J_flashMoreBtn')
input_second = browser.find_element_by_css_selector('#J_flashMoreBtn')
input_third = browser.find_element_by_xpath('//*[@id="J_flashMoreBtn"]')
print("first --> " + str(input_first))
print("second --> " + str(input_second))
print("third --> " + str(input_third))
browser.close()
