"""
数据库连接工具类
# """
import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection
from DBUtils.PersistentDB import PersistentDB, PersistentDBError, NotSupportedError

config = {
    'host': '13.209.87.201',
    'port': 3306,
    'database': 'wedo',
    'user': 'wedo',
    'password': '2708poem',
    'charset': 'utf8'
}


def get_db_pool(is_mult_thread):
    if is_mult_thread:
        poolDB = PooledDB(
            # 指定数据库连接驱动
            pymysql,
            # 指定最少连接数
            3,
            **config
        )
    else:
        poolDB = PersistentDB(
            # 指定数据库连接驱动
            pymysql,
            **config
        )
    return poolDB


if __name__ == '__main__':
    conn = get_db_pool(False).connection()
    cursor = conn.cursor()
    cursor.execute('select * from books')
    result = cursor.fetchone()
    print(result)
    conn.close()
