"""
NumPy模块练习
"""
import numpy as np

''' array函数 '''
# 使用列表创建
list1 = [1, 2, 3, 4, 5]
print('使用list创建:')
print(np.array(list1))

''' zeros创建全零数组 '''
print('生成全零数组: ', np.zeros(3))
print('生成多维的全零数组: ')
# print(np.zeros(3, 3))

''' ndarray其他创建方式'''
print(np.arange(20))

''' 合并操作 '''
score1 = np.array([
    [89, 90],
    [60, 60],
    [54, 53]
])
score2 = np.array([
    [100, 100],
    [111, 111],
    [120, 120]
])

# 水平方向的堆叠操作
print("水平方向的堆叠操作: np.hstack([score1, score2]) = %s " % np.hstack([score1, score2]))

# 垂直方向的堆叠操作
print("求垂直方向的堆叠操作: np.vstack([score1, score2]) = %s " % np.vstack([score1, score2]))

# 求以e为底数的对数
print("求以e为底数组的对数: np.log(score2) = %s" % np.log(score2))
# 求以2为底数的对数
print("求以2为底16的对数: np.log2(16) = %s" % np.log2(16))
# 求以1+x为底数的对数
print("求以1+x为底9的对数: np.log1p(9) = %s" % np.log1p(9))
# 求以10为底100的对数
print("求以10为底100的对数: np.log10(100) =  %s" % np.log10(100))

arr7  =np.array([6, 12, 24, 36, 48, 60])
arr8 = np.array([2, 3, 4, 6, 8, 11])
print(np.mod(arr7, arr8))

arr1 = np.random.randint(0, 101, [5, 5])
arr2 = np.random.randint(0, 101, [5, 5])

print("arr1 = %s" % arr1)
print("arr2 = %s" % arr2)

arr3 = np.where(arr1 > arr2, arr1, arr2)
print("arr3 = %s " % arr3)

arr4  = np.array([1,np.nan,np.inf,np.nan, 3, np.inf])
arr5 = np.where(np.isnan(arr4) | np.isinf(arr4), 0, arr4)
print("arr5 = %s" % arr5)

