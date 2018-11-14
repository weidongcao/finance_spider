# -*- coding:utf-8 -*-


class PropertiesUtil(object):
    # 缓存配置
    __conf__ = {}

    def __init__(self, file_path="application.properties"):
        """
        获取资源文件，形成字典
        :param file_path: 文件路径
        :return:字典内容的key、value均为字符串
        """
        with open(file_path, 'r', encoding='UTF-8') as pro_file:
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    value = line[len(strs[0]) + 1:]
                    self.__conf__[strs[0].strip(), value.strip()]

    def get_value(self, key):
        """
        获取指定配置属性值
        :param key: 属性名称
        :return: 返回字符串格式的属性值
        """
        return self.__conf__[key]

    def get_int_value(self, key):
        """
        获取指定配置属性值
        :param key: 属性名称
        :return: 返回int格式的属性值
        """
        return int(self.__conf__[key])


# 获取实例，保持单例
prop = PropertiesUtil()

if __name__ == "__main__":
    # 调用方式，获取实例
    # from util.ConfigUtil import prop
    ss = prop.get_value("host")

    print("ss = %s" % ss)