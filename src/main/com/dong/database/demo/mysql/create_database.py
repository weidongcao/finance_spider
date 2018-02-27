"""
通过Python，连接Mysql并创建数据库配置实例
"""
import pymysql

db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306)
cursor = db.cursor()
cursor.execute('select version()')
data = cursor.fetchone()
print('Database version: ', data)
cursor.execute('create database spiders default character set utf8 collate utf8_general_ci')
db.close()