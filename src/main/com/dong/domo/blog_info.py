"""
使用Python爬虫爬取自己博客的相关信息
"""
import json
import re

import pymysql
import requests


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    # pattern = re.compile(
    #     '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?'
    #     'name.*?<a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>'
    #     '(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
    #     re.S
    # )
    pattern = re.compile(
        '<li.*?blog-unit.*?details/(.*?)".*?<h3.*?>(.*?)</h3>.*?tag">(.*?)</div>'
        '.*?left-dis-24">(.*?)</div>.*?span>(.*?)</span>.*?</li>',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'bid': item[0].strip(),
            'publish_type': item[2].strip(),
            'publish_time': item[3].strip(),
            'title': item[1].strip()
            # 'index': item[0],
            # 'title': item[2].strip(),
            # 'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            # 'time' : item[4].strip()[5:] if len(item[4]) > 5 else '',
            # 'score': item[5].strip() + item[6].strip(),
            # 'image': item[1]
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


def write_to_mysql(bid, title, publish_type, publish_time):
    db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306, db='spiders', charset='utf8')
    cursor=db.cursor()
    sql = 'insert into blog(bid, title, publish_type, publish_time) values(%s, %s, %s, %s)'
    cursor.execute(sql, (bid, title, publish_type, publish_time))
    db.commit()
    db.close()


def main(offset):
    # url = 'http://maoyan.com/board/4?offset=' + str(offset)
    url = 'https://blog.csdn.net/daerzei'
    html = get_one_page(url)
    # print(html)
    items = parse_one_page(html)
    for item in items:
        # write_to_json(item)
        write_to_mysql(item["bid"], item["title"], item["publish_type"], item["publish_time"])


if __name__ == "__main__":
    # for i in range (10):
    #     main(offset=i * 10)
    main(None)
