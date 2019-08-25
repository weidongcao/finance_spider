import tensorflow as tf
import pandas as pd
from matplotlib import pyplot as plt

import numpy as np

df = pd.read_csv(open('huoyunliang.csv', encoding='utf-8'))

data = np.array(df['铁路客运量_当期值(万人)'])
# 标准化
normalized_data = (data - np.mean(data)) / np.std(data)

# 2.模型构建
# (1)输入层 - 每次输出多少数据
# (2)输出层 - 每次输出多少数据
# 我是拿多个值预测一个值呢,不是拿多个值预测多个值
# 准备用3个月的数据预测后面3个月的数据
#   前者 --> rnn_output  只取最后那个时刻输出的结果
#   后者 --> rnn_output每一个输出都使用到
time_size = 3
input_size = 1
hidden_size = 128
# rnn输入的shape[batch_size, time_size, input_size]
X = tf.placeholder(tf.float32, [None, time_size, input_size])
Y = tf.placeholder(tf.float32, [None, time_size])

train_x, train_y = [], []
for i in range(len(normalized_data) - time_size - 1):
    train_x.append(np.expand_dims(normalized_data[i:i + time_size], axis=1).tolist())
    train_y.append(normalized_data[i + 1: i + time_size + 1].tolist())


def rnn_net():
    # cell 节点构建
    cell = tf.nn.rnn_cell.GRUCell(hidden_size)
    outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

    # outputs [batch_size, time_size, hidden_size]
    # => batch_size, time_size
    W = tf.Variable(tf.random_normal(hidden_size, 1))
    b = tf.Variable(tf.random_normal([1]))
    # 扩增W, 变成一个三维的W = V
    w_repeated = tf.tile(tf.expand_dims(W, 0), [tf.shape(X)[0], 1, 1])
    out = tf.matmul(outputs, w_repeated) + b
    return tf.squeeze(out)


def train():
    pre = rnn_net()
    loss = tf.reduce_mean(tf.square(pre -Y))
    lr = 0.0001
    # 自适应学习率
    global_step = tf.Variable(0)
    learning_rate = tf.train.exponential_decay(lr, global_step=global_step, learning_rate=10000, decay_rate=0.96, staircase=True)
    train_op = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss, global_step=global_step)
    with tf.Session as sess:
        sess.run(tf.global_variables_initializer())
        writer = tf.summary.FileWriter('log', sess.graph)
        saver = tf.train.Saver()
        for i in range(100000):
            _, loss_ = sess.run([train_op, loss], feed_dict={X:train_x, Y:train_y})
            if i % 100 == 0:
                print(i, loss)
            saver.save()


    train_op = tf.train.GradientDescentOptimizer(learning_rate=lr).minimize(loss)
# train()
def prediction():
    pre = rnn_net()
    saver = tf.train.Saver()
    with tf.Session as sess:
        saver.restore(sess, 'model/gru.model')
        prev_seq = train_x[-1]
        pred_list = []
        for i in range(12):
            next_seq = sess.run(pre, feed_dict={X:[prev_seq]})
            pred_list.append(next_seq)
            prev_seq = np.vstack((prev_seq[0:], next_seq[-1]))
        plt.figure()
        plt.plot(list(range(len(normalized_data))), normalized_data, color='b')
        plt.plot(list(range(len(normalized_data), len(normalized_data) + len(pred_list))), pred_list, color='r')
        plt.show()

prediction()