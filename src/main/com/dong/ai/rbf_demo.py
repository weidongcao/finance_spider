import tensorflow as tf
from tensorflow.examples

im_dim = 784
n_classes=10
hidden_size_1 = 256
hidden_size_2 = 128

# 数据占位符
x = tf.placeholder(tf.float32, [None, in_dim])
y = tf.placeholder(tf.float32, [None, n_classes])

# 设置权重和偏执量
weights = {
    'w1':tf.Variable(tf.random_normal([in_dim, hidden_size_1], stddev=0.1))
    'w2':tf.Variable(tf.random_normal([hidden_size_1, hidden_size_2], stddev=0.1))
}

bias = {
    'b1':tf.Variable(tf.random_normal([hidden_size_1], stddev=0.1))
    'b2': tf.Variable(tf.random_normal([hidden_size_2], stddev=0.1))
}

def net():
    # 第一个隐层

