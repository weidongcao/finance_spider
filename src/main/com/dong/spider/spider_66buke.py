"""
使用Python爬虫爬取自己指定66buke网小说
"""
import json

import requests
from bs4 import BeautifulSoup as bs
import re

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    ),
    "Referer": "https://www.66buke.com/book/28164/"
}


def parse_page_index(url):
    html = requests.get(url, headers=headers)
    soup = bs(html.text, 'lxml')
    book_text = soup.select("#BookText")[0].get_text()

    return book_text


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
    url_template = "https://www.66buke.com/book/28164/{bid}.html"
    page_index = 1
    book_text = ''

    for bid in range(20):
        url = url_template.format(bid=str(bid))
        print('url --> {}'.format(url))
        section_text = parse_page_index(url)
        flag = True if '点击下一页继续阅读' in section_text else False
        # 处理文本
        section_text = handle_text(section_text)
        book_text += section_text
        while flag:
            page = str(bid) + '_' + str(page_index)
            page_index += 1
            url = url_template.format(bid=str(page))
            print('url --> {}'.format(url))
            section_text = parse_page_index(url)
            flag = True if '点击下一页继续阅读' in section_text else False
            # 处理文本
            section_text = handle_text(section_text)
            book_text += section_text
        page_index = 1

    print(book_text)
    # with open('66buke.txt', 'a', encoding='utf-8', newline='') as file:
    #     file.write(book_text)


def handle_text(text):
    text = text.replace('本章未完，点击下一页继续阅读', '')
    text = text.replace('点击下一页继续阅读', '')
    text = re.sub('[\n]+', '\n', text)
    line_list = text.split('\n')
    text = ''
    for line in line_list:
        line = line.strip()
        text += line
        text += '\n'
        if '\t' in line:
            text += '\n'
    return text


if __name__ == "__main__":
    #
    main()
