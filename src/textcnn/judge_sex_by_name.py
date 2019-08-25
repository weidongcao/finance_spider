import pandas as pd
data = pd.read_csv('name.csv')
# 构建数据集
train_x = []
train_y = []

for row in data.values:
    name = row[1]
    label = row[2]
    train_x.append(name)
    # if label == 0:

