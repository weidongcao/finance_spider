"""
使用Python爬虫爬取自己博客统计CSDN所有博客总的浏览量
"""
import json
import re
import sys

from com.dong.entity.Csdn import Csdn
# from com.dong.utils.DbPoolUtil import dbpool


def parse_page_index(html):
    p = re.compile(
        'item-tiling.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?grade-box.*?title="(.*?)级.*?title="(.*?)".*?title="(.*?)".*?title="(.*?)".*?</div>',
        re.S
    )
    summaries = re.findall(p, html)
    # return summaries
    for s in summaries:
        # print(s)
        yield {
            Csdn(None, None, s[0].strip(), s[1].strip(), s[2].strip(), s[3].strip(), s[4].strip(), s[5].strip(),
                 s[6].strip(), s[7].strip())
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


def main():
    if sys.platform.__eq__("linux"):
        file_path = "/opt/data/myblog/daerzei.html"
    elif sys.platform.__eq__("win32"):
        file_path = "D:\\0WorkSpace\\atom\\myblog\\daerzei.html"
    else:
        return

    with open(
            file_path,
            'r',
            encoding='utf-8'
    ) as html_src:
        content = html_src.read()

    csdns = parse_page_index(content)

    for csdn_set in csdns:
        for csdn in csdn_set:
            # write_to_json(visit)
            print(csdn.__str__())
            # dbpool.execute_iud(csdn.insert_sql())


if __name__ == "__main__":
    main()
