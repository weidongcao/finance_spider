"""
使用Python爬虫爬取自己博客统计不同的博客的浏览量
升级版
"""
import json
import re

import requests

from com.dong.entity.Csdn import Csdn
from com.dong.utils.DbPoolUtil import dbpool


def parse_page_index(html):
    p = re.compile(
        (
            'item-tiling.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?'
            'grade-box.*?title="(.*?)级.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?</div>'
        ),
        re.S
    )
    items = re.findall(p, html)
    for s in items:
        yield Csdn(
                None, None, s[0].strip(),
                s[1].strip(), s[2].strip(),
                s[3].strip(), s[4].strip(),
                s[5].strip(), s[6].strip(), s[7].strip()
        )


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
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
        ),
        "Referer": "https://blog.csdn.net/"
    }
    main_page = "https://blog.csdn.net/daerzei"
    url = main_page

    # print("url = %s" % url)
    # print("headers = %s" % headers)

    response = requests.get(url, headers=headers)
    csdns = parse_page_index(response.text)

    cdsn_data = []
    for csdn in csdns:
        print(csdn.insert_sql())
        cdsn_data.append(csdn.__data__())
    dbpool.execute_many_iud(Csdn.insert_temple, cdsn_data)


if __name__ == "__main__":
    #
    main()

