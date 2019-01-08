"""
使用Python爬虫爬取自己指定博客的信息并存入Mysql数据库
"""
import json

import requests

from com.dong.utils.str_utils import str_count
from com.dong.entity.Blog import Blog
from com.dong.utils.DbPoolUtil import dbpool
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    ),
    "Referer": "https://blog.csdn.net/"
}


def parse_page_index(response):
    soup = bs(response.text, 'lxml')
    publish_type = soup.select(".article-type")[0].get_text()

    title = soup.select(".title-article")[0].get_text()
    publish_time = soup.select(".time")[0].get_text()
    publish_time = publish_time.replace("年", "-")
    publish_time = publish_time.replace("月", "-")
    publish_time = publish_time.replace("日", "-")
    url = response.url

    count = str_count(soup.select("#content_views")[0].get_text())

    return Blog(url[-8:].strip(), url.strip(), publish_type.strip(), title.strip(), publish_time.strip(), count.zh + count.en + count.digit + count.punc)


def write_to_json(content):
    """
    将提取的结果写入文件，这里直接写入到一个文本文件中，通过json库的dumps()方法
    实现字典的序列化，并指定ensure_ascii参数为False，这样可以保证输出的结果是
    中文形而不是Unicode编码
    :param content:
    :return:
    """
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False, ) + '\n')


def main():

    bid = 85294450
    url_template = "https://blog.csdn.net/daerzei/article/details/{bid}"
    url = url_template.format(bid=str(bid))
    response = requests.get(url, headers=headers)
    info = parse_page_index(response)

    dbpool.execute_iud(Blog.insert_temple, info.__data__())


if __name__ == "__main__":
    #
    main()