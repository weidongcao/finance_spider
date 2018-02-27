"""
测试Python连接MySQL

"""
import pymysql
db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', db='spiders')
cursor = db.cursor()
# 创建Mysql数据库表
sql = 'create table if not exists students (sid VARCHAR(255) not NULL , sname VARCHAR(255) not NULL, age int, PRIMARY KEY (sid))'
cursor.execute(sql)
db.close()