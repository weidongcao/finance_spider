"""
向Mysql数据插入数据
"""
import pymysql
sid = '30000122708'
sname = 'Dong'
age = 19
db = pymysql.connect(host='cm02.spark.com', user='root', password='123123', port=3306, db='spiders')
cursor=db.cursor()
sql = 'insert into students(sid, sname, age) values(%s, %s, %s)'
try:
    cursor.execute(sql, (sid, sname, age))
    db.commit()
except:
    print('fail')
    db.rollback()
db.close()
