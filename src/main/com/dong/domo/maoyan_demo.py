"""
利用Requests和正则表达式来抓取独眼电影TOP100的相关内容，
Requests相较于Urllib使用更加方便，而且目前我们还没有
系统学习HTML解析库，所以可能对HTML的解析库不是很了解，
所以本节我们选用正则表达式来作为解析工具
目标：
    提取出独眼电脑TOP100榜的电影名称、时间、评分、图片等信息
    提取的站点URL为：http://maoyan.com/board/4，
    提取的结果我们以文件形式下来。
"""
import json
import re

import requests


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?'
        'name.*?<a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>'
        '(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time' : item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip(),
            'image': item[1]
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


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    items = parse_one_page(html)
    for item in items:
        write_to_json(item)


if __name__ == "__main__":
    for i in range (10):
        main(offset=i * 10)
