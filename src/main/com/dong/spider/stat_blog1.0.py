"""
使用Python爬虫爬取自己博客统计不同的博客的浏览量
升级版
"""
import json
import re

import requests

from com.dong.utils.str_utils import str_count
from com.dong.entity.Blog import Blog
from com.dong.utils.DbPoolUtil import dbpool
from bs4 import BeautifulSoup as bs

main_page = "https://blog.csdn.net/daerzei"
url_template = "https://blog.csdn.net/daerzei/article/list/{page}"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    ),
    "Referer": "https://blog.csdn.net/"
}


def get_blog_info(html):
    pattern = re.compile(
        (
            'article-item-box.*?data-articleid="(.*?)"'
            '.*?<h4.*?href="(.*?)"'
            '.*?article-type.*?>(.*?)'
            '</span>(.*?)</a>'
            '.*?align-content-center.*?'
            'class="date">(.*?)</span>.*?评论数'
        ),
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        if item[1].strip().__contains__("daerzei") and (item[2] != "转"):
            response = requests.get(item[1].strip(), headers=headers)
            # print(response.text)

            soup = bs(response.text, 'lxml')
            content = soup.select("#content_views")[0].get_text()
            # print("len(content) = ", len(content))

            count = str_count(content)
            yield Blog(item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip(), item[4].strip(), count.zh + count.en + count.digit + count.punc)


def get_page_list(response):
    page_info = []
    pattern = re.compile(
        (
            "baseUrl = '(.*?)'"
            ".*?var pageSize =(.*?);"
            ".*?listTotal =(.*?);"
         ),
        re.S
    )
    items = re.findall(pattern, response)

    return page_info


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
    response = requests.get(main_page, headers=headers)

    # 获取页数
    page_list = get_page_list(response)
    print(page_list)
    exit(0)
    # 抓取的博客信息
    visit_data = []

    for index in page_list:
        url = url_template.format(page=str(index))

        response = requests.get(url, headers=headers)
        info_list = get_blog_info(response.text)

        for visit in info_list:
            print(visit.__str__())
            visit_data.append(visit.__data__())
    # 反转列表
    visit_data.reverse()
    # 写入数据库
    dbpool.execute_many_iud(Blog.insert_temple, visit_data)


if __name__ == "__main__":
    #
    main()

