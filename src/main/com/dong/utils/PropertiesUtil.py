# -*- coding:utf-8 -*-


class PropertiesUtil(object):
    # 缓存配置
    __file_dict = {}

    def get_config_dict(self, file_path="pdbc.properties"):
        """
        获取资源文件，形成字典
        :param file_path: 文件路径
        :return:字典内容的key、value均为字符串
        """
        if file_path not in self.__file_dict:
            properties = {}
            with open(file_path, 'r', encoding='UTF-8') as pro_file:
                for line in pro_file.readlines():
                    line = line.strip().replace('\n', '')
                    if line.find('=') > 0 and not line.startswith('#'):
                        strs = line.split('=')
                        value = line[len(strs[0]) + 1:]
                        self.__get_dict(strs[0].strip(), properties, value.strip())
            self.__file_dict[file_path] = properties
        return self.__file_dict[file_path]

    def get_config_value(self, file_path, prop_name):
        """
        获取资源文件，形成字典，获取属性值
        :param file_path: 文件路径
        :param prop_name: 属性名称
        :return: 返回字符串格式的属性值
        """
        return self.get_config_dict(file_path)[prop_name]

    def __get_dict(self, dict_name, properties, value):
        """
        递归获取配置字典
        :param dict_name:键
        :param properties: 字典
        :param value: 值
        :return:
        """
        if dict_name.find('.') > 0:
            key = dict_name.split('.')[0]
            properties.setdefault(key, {})
            self.__get_dict(dict_name[len(key) + 1:], properties[key], value)
        else:
            properties[dict_name] = value


# 获取实例，保持单例
prop = PropertiesUtil()

if __name__ == "__main__":
    # 调用方式，获取实例
    # from util.ConfigUtil import prop
    print(prop.get_config_dict("pdbc.properties"))
    print(prop.get_config_value("pdbc.properties", "host"))