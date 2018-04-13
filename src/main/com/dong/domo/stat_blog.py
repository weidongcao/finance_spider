"""
使用Python爬虫爬取自己博客的浏览量
"""
import json
import re

import pymysql
import requests

from com.dong.domo.Csdn import Csdn
from com.dong.domo.Visit import Visit


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page_list(html):
    pattern = re.compile(
        '<li.*?blog-unit.*?details/(.*?)".*?span>(.*?)</span>.*?</li>',
        re.S
    )
    visits = re.findall(pattern, html)
    for visit in visits:
        yield{
            Visit(None, visit[0].strip(), visit[1].strip())
            # 'bid': item[0].strip(),
            # 'read_cnt': item[1].strip()
        }


def parse_one_page_summary(sss):
    p = re.compile(
        'div.*?inf_number_box.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?interflow.*?title="(.*?)级.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?</div>',
        re.S
    )
    summaries = re.findall(p, sss)
    # return summaries
    for s in summaries:
        # print(s)
        yield{
            Csdn(None, None, s[0].strip(), s[1].strip(), s[2].strip(), s[3].strip(), s[4].strip(), s[5].strip(), s[6].strip(), s[7].strip())
            # 'original': s[0].strip(),
            # 'fans': s[1].strip(),
            # 'liked': s[2].strip(),
            # 'comments': s[3].strip(),
            # 'level': s[4].strip(),
            # 'visit': s[5].strip(),
            # 'score': s[6].strip(),
            # 'rank': s[7].strip()
        }


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


def blog_write_to_mysql(visit):
    db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306, db='spiders', charset='utf8')
    cursor = db.cursor()
    cursor.execute(visit.insert_sql)
    db.commit()
    db.close()


def csdn_write_to_mysql(csdn):
    db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306, db='spiders', charset='utf8')
    cursor = db.cursor()
    cursor.execute(csdn.insert_sql)
    db.commit()
    db.close()


def main(offset):
    # url = 'http://maoyan.com/board/4?offset=' + str(offset)
    url = 'https://blog.csdn.net/daerzei'
    html = get_one_page(url)
    # print(html)
    items = parse_one_page_list(html)
    total_visit = 0
    for item in items:
        for visit in item:
            blog_write_to_mysql(visit)
            total_visit += int(visit.read_cnt)

    csdns = parse_one_page_summary(html)
    for item in csdns:
        for csdn in item:
            csdn.visit = total_visit
            csdn_write_to_mysql(csdn)
        # print(csdn)


if __name__ == "__main__":
    # for i in range (10):
    #     main(offset=i * 10)
    main(None)
    # url = 'https://blog.csdn.net/daerzei'
    # html = get_one_page(url)
    # items = parse_one_page_list(html)
    # print(items)

