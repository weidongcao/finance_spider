import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from skimage.io import imsave
import os
import shutil


# mnist数据集读取进来
mnist = input_data.read_data_sets('data')

# 建立网络结构参数
img_height = 28
img_width = 28
img_size = img_height * img_width

# fake数据保存路径
output_path = 'output'
max_epoch = 500

# 神经网络参数
h1_size = 150   # --> 第一个隐藏层
h2_size = 300   # --> 第二个隐藏层
z_size = 100    # --> 噪声
batch_size = 64

x_data = tf.placeholder(tf.float32, [batch_size, img_size])
z_prior = tf.placeholder(tf.float32, [])
keep_prob = tf.placeholder(tf.float32)

# 构建生成器，bp网络
z_prior = tf.placeholder(tf.float32, [batch_size, z_size])
def build_generator(z_prior):
    w1 = tf.Variable(tf.truncated_normal([z_size, h1_size], stddev=0.1))
    b1 = tf.Variable(tf.truncated_normal([h1_size], stddev=0.1))
    h1 = tf.nn.relu(tf.nn.xw_plus_b(z_prior, w1, b1))

    w2 = tf.Variable(tf.truncated_normal([h1_size, h2_size], stddev=0.1))
    b2 = tf.Variable(tf.truncated_normal([h2_size], stddev=0.1))
    h2 = tf.nn.relu(tf.nn.xw_plus_b(h1, w2, b2))

    w3 = tf.Variable(tf.truncated_normal([h2_size, img_size], stddev=0.1))
    b3 = tf.Variable(tf.truncated_normal([img_size], stddev=0.1))
    x_generate = tf.nn.relu(tf.nn.xw_plus_b(h2, w3, b3))

    g_params = [w1, b2, w2, b2, w3, b3]
    return x_generate,g_params


# 构建判别器，bp网络
def build_discriminator(x_data, x_generate, keep_prob):
    x_in = tf.concat([x_data, x_generate], 0)

    w1 = tf.Variable(tf.truncated_normal([img_size, h2_size], stddev=0.1), name='g_w1')
    b1 = tf.Variable(tf.truncated_normal([h2_size]), name='g_b1')
    h1 = tf.nn.dropout(tf.nn.relu(tf.nn.xw_plus_b(x_in, w1, b1)), keep_prob, name='g_h1')

    w2 = tf.Variable(tf.truncated_normal([h2_size, h1_size], stddev=0.1), name='g_w2')
    b2 = tf.Variable(tf.truncated_normal([h1_size], stddev=0.1), name='g_b2')
    h2 = tf.nn.dropout(tf.nn.relu(tf.nn.xw_plus_b(h1, w2, b2)), keep_prob, name='g_h2')

    w3 = tf.Variable(tf.truncated_normal([h1_size, 1], stddev=0.1), name='g_w3')
    b3 = tf.Variable(tf.zeros([1]), name='g_b3')
    h3 = tf.nn.xw_plus_b(h2, w3, b3, name='g_h3')

    y_data = tf.nn.sigmoid(tf.slice(h3, [0, 0], [batch_size, -1]))
    y_generated = tf.nn.sigmoid(tf.slice(h3, [batch_size, 0], [-1,-1]))

    g_params = [w1, b1, w2, b2, w3, b3]
    return x_generate, g_params

# 16 * 16
# grid_pad -->每一个格子间距上下为5
# gen_val.shape: --> [batch, img_size]
def save_result(gen_val, filename, grid_size=(8, 8), grid_pad=5):
    val_data = gen_val.reshape(gen_val.shape[0], img_height, img_width)
    # 实际框的高度
    grid_h = img_height * grid_size[0] + grid_pad* (grid_size[0] - 1)
    grid_w = img_width * grid_size[1] + grid_pad * (grid_size[1] - 1)

    img_grid = np.zeros([grid_h, grid_w], np.uint8)
    for i, res in enumerate(val_data):
        if i >= grid_size[0] * grid_size[1]:
            break
        img = res * 255
        img = img.astype(np.uint8)
        row = (i % grid_size[0]) * (img_height + grid_pad)
        col = (i % grid_size[1]) * (img_width + grid_pad)

        img_grid[row:row + img_height, col: col + img_width] = img



def train():
    # 调用生成模型
    x_generated, g_params = build_generator(z_prior)
    # 调用判别模型
    y_data, y_generated, d_params = build_discriminator(x_data, x_generated, keep_prob)

    # 构建生成器损失
    g_loss = -tf.log(y_generated)
    d_loss = -(tf.log(y_data) + tf.log(1 - y_generated))

    # 构建生成器优化函数,传入生成器变量参数
    optimizer = tf.train.AdamOptimizer(0.0001)
    g_trainer = optimizer.minimize(g_loss, var_list=g_params)

    # 构建差别器函数,传入判别器变量参数
    d_trainer = optimizer.minimize(d_loss, var_list=d_params)

    # 迭代训练,训练再次的D,一次的G
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # 持久化模型
        saver = tf.train.Saver()
        # 断点续训
        ckpt_file = tf.train.latest_checkpoint('model')
        if ckpt_file:
            saver.restore(sess, ckpt_file)

        steps = mnist.train.num_examples // batch_size

        for i in range(max_epoch):
            for j in range(steps):
                print('Epoch: {}-iter: {}'.format(i, j))
                x_value, _ = mnist.train.next_batch(batch_size)
                z_value = np.random.normal(0, 1, size=[batch_size, z_size])

                # 执行判别器的优化
                sess.run(d_trainer, feed_dict={x_data:x_value, z_prior: z_value, keep_prob:0.7})

                if j % 1 == 0:
                    sess.run(g_trainer, feed_dict={x_data:x_value, z_prior: z_value, keep_prob:0.7})

                # 保存生成器生成的数据为图片,存在酵磁盘中,作为人为判断跟上训练的依据
                x_gen_val = sess.run(x_generated, feed_dict={z_prior: z_value})
                save_result(x_gen_val, os.path.join(output_path, 'smaple{}.jpg'.format(i)))
                # 再去生成一个随机的正态分布的噪声,相当于是测试数据
                z_test_value = np.random.normal(0, 1, size=[batch_size, z_size])
                x_test_gen_val = sess.run(x_generated, feed_dict={z_prior: z_test_value})

                save_result(x_gen_val, os.path.join(output_path, 'smaple{}.jpg'.format(i)))