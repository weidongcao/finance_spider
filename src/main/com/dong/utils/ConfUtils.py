"""
Python配置文件操作工具类
读取cnf.ini配置文件
"""
import configparser as cp

import os


def get_conf():
    conf_file = "cnf.ini"
    conf_dir = os.path.dirname(os.path.abspath(__file__))
    CONF_FILE = os.path.join(conf_dir, conf_file)
    # print("conf_file = %s" % CONF_FILE.__str__())
    # print("type(CONF_FILE) = %s" % type(CONF_FILE))
    cnf = cp.ConfigParser()
    cnf.read(CONF_FILE, encoding='utf-8')
    return cnf


conf = get_conf()


if __name__ == '__main__':
    # 获取所有块
    print("cnf.sections() = %s" % conf.sections())
    # 获取指定块,指定键的值
    print("cnf.get('mysql', 'host')) = %s" % conf.get('mysql', 'host'))
    # 获取指定块的所有配置
    print("cnf.items('mysql') = %s" % conf.items('mysql'))
    # 获取指定块,指定键的值,返回int类型
    print("cnf.getint('mysql', 'port') = %s " % conf.getint('mysql', 'port'))
    # 判断指定节点是否存在
    print("cnf.has_section('mysql') = %s" % conf.has_section('mysql'))
    # 判断指定节点的配置是否存在
    print("cnf.has_option('mysql', 'host') = %s " % conf.has_option('mysql', 'host'))

    # 添加一个块
    # cnf.add_section('wedo')
    # cnf.add_section('weidong')

    # 添加一个配置
    # cnf.set('mysql', 'password', 'xxxxxxxx')
    # cnf.write(open('cnf.ini', 'w'))

    # 删除一个块
    # cnf.remove_section('test')
    # cnf.write(open('cnf.ini', 'w'))










