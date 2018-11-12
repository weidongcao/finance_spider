"""
pandas模块练习
"""
import numpy as np
import pandas as pd
# 列表创建,如果没有指定index,那么会从0开始计数
ser1 = pd.Series(["Tom", "Jerry", "Li", "Wang"])

# 使用字典创建,字典的key会当成series的index(索引)
ser2 = pd.Series({"one":"Tom", "two":"Jerry", "three":"Li", "four":"Wang"})

# 设置Name属性
ser2.name = '姓名'
print("ser2.name = %s" % ser2.name)
# 设置索引的名称
ser2.index.name = "序列"
print("ser2.index.name = %s" % ser2.index.name)

print("ser2.axes = %s" % ser2.axes)
print("ser2.index = %s" % ser2.index)

ser3 = pd.Series(np.array([1, 2, 3, 4, 5]), dtype="float")

# 获取Series的索引
print("ser3.index = %s" % ser3.index)

# 获取Series的值
print("ser3.values = %s" % ser3.values)

score = np.random.randint(0, 101, 36)
print(score)
print(pd.Series.sort_values(score))