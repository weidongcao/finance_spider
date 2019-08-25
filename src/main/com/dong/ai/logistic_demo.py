"""
乳腺癌分类
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import sklearn
from sklearn.linear_model import LogisticRegressionCV, LinearRegression
from sklearn.linear_model.coordinate_descent import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# set font sets
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# intercept exception
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)

# 数据读取并处理异常数据
path = "datas/breast-cancer-wisconsin.data"
names = ['id', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
         'Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei',
        'Bland Chromatin','Normal Nucleoli','Mitoses','Class']
df = pd.read_csv(path, header=None, names=names)
# 只要有列为空,就进行删除操作
datas = df.replace('?', np.nan).dropna(how='any')

# 显示一下
# print(datas.head(5))
# print(datas.dtypes)
print(datas['Bare Nuclei'].value_counts())

# 1. 数据提取以及数据分隔
# 提取
X = datas[names[1:10]]
Y = datas[names[10]]

# 分隔
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

# 2. 数据模式化(归一化)
ss = StandardScaler()
# 训练模型及归一化数据
X_train = ss.fit_transform(X_train)

# 3. 模型构建及训练
# penalty:过拟合解决参数,l1或者l2
# solver: 参数优化方式
# 当penalty为l1的时候,参数只能是:liblinear(坐标轴下降法)
# nlbfgs和cg都是关于目标函数的魂不二阶泰勒展开
# 当penalty为l2的时候可以是:lbfgs(拟牛顿法),newton-cg(牛顿法变种),seg(minibatch)
# 维度<10000时,lbfgs 维度>10000时,cg法比较好,显卡计算的时候,lbfgs和cg都比seg快
# multi_class:分类方式参数;参数可选:ovr(默认),multinomial;这两种方式在二元分类问题中,
# 效果是一样的;在多元分类问题中效果不一
# ovr:one-vs-rest,对于多元分类的问题,先将其看作二元分类,分类完成后,再迭代对其中一类继续进行二元分类
# multinomial:many-vs-many(MVM),对于多元分类问题,如果模型有T类,我们每次在所有的T类样本里面选择两类
# 样本出来,
# 不妨记为T1类和T2类,把所有的输出为T1和T2的样本放在一起,把T1作为正例,T2作为负例.
# 进行二元逻辑回归,得到模型参数,我们一共需要T(T-1)/2次分类
# class_weight:特征权重参数
#
# TODO:Logistic回归是一种分类算法,不能应用于回归中(也既是说对于传入模型的y值来讲,不能是float类型,必须是int类型
#
lr = LogisticRegressionCV(multi_class='ovr', fit_intercept=True, Cs=np.logspace(-2, 2, 20), cv=2, penalty='l1', solver='liblinear', tol=0.01)
re = lr.fit(X_train, Y_train)

# 4. 模型效果获取
r = re.score(X_train, Y_train)
print("准确率: ", r)
print("稀疏化特征比率: %.2f%%" % (np.mean(lr.coef_.ravel() == 0) ** 100))
print("参数: ", re.coef_)
print("截距: ", re.intercept_)
print(re.predict(X_train))
y_hat = re.predict(X_train)
print(y_hat)

print(lr.decision_function(X_train))

# 5. 模型相关信息保存
# 引入包
# from sklearn.externals import  joblib
# 要求文件夹必须存在
# 将标准化模型保存
# joblib.dump(ss, "datas/logistic/ss.model")
# 将模型保存
# joblib.dump(lr, "datas/models/logistic/lr.model")

# 模型加载
# 引入包
# from sklearn.externals import joblib
# oss = joblib.load(("models/logistic/ss.model"))
# olr = joblib.load("models/logistic/lr.model")

# 数据预测
# a.预测数据格式化(归一化)
# 使用模型进行归一化操作
X_test = ss.transform(X_test)

# b.结果数据预测
Y_predict = re.predict(X_test)

# c.图表展示
x_len = range(len(X_test))
plt.figure(figsize=(14, 7), facecolor='w')
plt.ylim(0, 6)
plt.plot(x_len, Y_test, 'ro', markersize=8, zorder=3, label=u'真实值')
plt.plot(x_len, Y_predict, 'go', markersize=14, zorder=2, label=u'预测值,准确率=%.3f' % re.score(X_test, Y_test))
plt.legend(loc='upper left')
plt.xlabel(u'数据编号', fontsize=18)
plt.ylabel(u'乳腺癌类型', fontsize=18)
plt.title(u'Logistic回归算法对数据进行分类', fontsize=20)
plt.show()




