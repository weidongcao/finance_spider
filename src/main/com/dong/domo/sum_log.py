import re


def main(args):
    # 正则表达式匹配需要文本
    # 例如: from database get 123 items
    p = re.compile("from reg_realid_info where last_logintime.*?to_date.*?'(.*?)'.*?to_date.*?'(.*?)'.*?从 reg_realid_info 取到到 (.*?) 条数据.*?写入Solr (.*?) 条数据", re.S)
    # 读取文件内容
    with open("log.log", 'r', encoding='utf-8') as log:
        content = log.read()
    # 匹配查找所有
    summaries = re.findall(p, content)

    for sss in summaries:
        print(sss[0] + "\t\t" + sss[1] + "\t\t" + sss[2] + "\t\t" + sss[3])
        # if not sss[0].__eq__(sss[1]):
        #     print("oracle -> " + sss[0] + "\r\nsolr   -> " + sss[1])


if __name__ == "__main__":
    main(None)