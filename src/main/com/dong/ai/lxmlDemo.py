"""
lxml,Xpath模块学习

Xpath语法:

"""
import requests
from lxml import etree

from lxml.html import etree

url = "https://blog.csdn.net/daerzei"
header = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
	"Referer":"https://blog.csdn.net/daerzei?orderby=ViewCount"
}
response = requests.get(url, header)
print(response.text)
