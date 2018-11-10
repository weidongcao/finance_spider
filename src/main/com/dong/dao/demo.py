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
    config = {
        'host': '192.168.0.101',
        'port': 3306,
        'database': 'wedo',
        'user': 'wedo',
        'password': 'xxxxxx',
        'charset': 'utf8'
    }
    db_pool = PersistentDB(pymysql, **config)
    # 从数据库连接池是取出一个数据库连接
    conn = db_pool.connection()
    cursor = conn.cursor()
    # 来查下吧
    cursor.execute('select * from books')
    # 取一条查询结果
    result = cursor.fetchone()
    print(result)
    # 关闭连接,其实不是关闭,只是把该连接返还给数据库连接池
    conn.close()
