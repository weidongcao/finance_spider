"""
使用Python爬虫爬取自己博客的浏览量
"""
import datetime
import json
import re

import pymysql
import requests


def write_to_mysql(cdate, visit, score, rank, num):
    db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306, db='spiders', charset='utf8')
    cursor = db.cursor()
    sql = 'insert into csdn(cdate, visit, score, rank, num) values(%s, %s, %s, %s, %s)'
    cursor.execute(sql, (cdate, visit, score, rank, num))
    db.commit()
    db.close()


def main(offset):
    with open("result.txt", 'r') as content:
        while True:
            line = content.readline()
            if not line:
                break
                pass
            values = line.split("\t")
            write_to_mysql(values[0], values[1], values[2], values[3].replace("W+", ""), values[4].replace("\n", ""))


if __name__ == "__main__":
    # for i in range (10):
    #     main(offset=i * 10)
    main(None)
