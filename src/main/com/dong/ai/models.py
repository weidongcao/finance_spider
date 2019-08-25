import tensorflow as tf


# 网络
def inference(images, batch_size, n_classes):
    with tf.variable_scope('conv1') as scope:
        weithts = tf.get_variable('weights', shape=[3,3,3,16], initializer=tf.truncated_normal_initializer(stddev=0.1))
        biases = tf.get_variable('biases', shape=16, initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv = tf.nn.conv2d(images,weithts, strides=[1,1,1,1], padding='SAME')
        pre_activation = tf.nn.bias_add(conv,biases)
        net = tf.nn.relu(pre_activation)

    with tf.variable_scope('pooling1_lrn') as scope:
        pool = tf.nn.max_pool(net, ksize=[1,3,3,1], strides=[1,2,2,1], padding='SAME')
        norm=tf.nn.lrn(pool, depth_radius=4, bias=1, alpha=0.001/9, beta=0.75)

    with tf.variable_scope('conv2') as scope:
        weithts = tf.get_variable('weights', shape=[3,3,16, 32], initializer=tf.truncated_normal_initializer(stddev=0.1))

    with tf.variable_scope('conv1') as scope:
        weithts = tf.get_variable('weights', shape=[3, 3, 3, 16],
                                  initializer=tf.truncated_normal_initializer(stddev=0.1))
        biases = tf.get_variable('biases', shape=16, initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv = tf.nn.conv2d(images, weithts, strides=[1, 1, 1, 1], padding='SAME')
        pre_activation = tf.nn.bias_add(conv, biases)
        net = tf.nn.relu(pre_activation)

    with tf.variable_scope('pooling1_lrn') as scope:
        pool = tf.nn.max_pool(net, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
        norm = tf.nn.lrn(pool, depth_radius=4, bias=1, alpha=0.001 / 9, beta=0.75)

    with tf.variable_scope('conv2') as scope:
        weithts = tf.get_variable('weights', shape=[3, 3, 16, 32],
                                  initializer=tf.truncated_normal_initializer(stddev=0.1))

    with tf.variable_scope('flatten') as scope:
        reshape = tf.reshape(pool, shape=[batch_size, -1])
        dim = reshape.get_shape()[1].value

    with tf.variable_scope('fc1'):
        weithts = tf.get_variable('weights', shape=[128],initializer=tf.truncated_normal_initializer(stddev=0.005))
        biases = tf.get_variable('biases', shape=[128], initializer=tf.truncated_normal_initializer(stddev=0.1))
        fc = tf.nn.relu(tf.matmul(reshape, weithts) + biases)

    with tf.variable_scope('fc2'):
        weithts = tf.get_variable('weights', shape=[128,64], initializer=tf.truncated_normal_initializer(stddev=0.005))
        biases = tf.get_variable('biases', shape=[64], initializer=tf.truncated_normal_initializer(stddev=0.1))
        fc = tf.nn.relu(tf.matmul(reshape, weithts) + biases)

    with tf.variable_scope('softmax_linear'):
        with tf.variable_scope('fc2'):
            weithts = tf.get_variable('weights', shape=[128], initializer=tf.truncated_normal_initializer(stddev=0.005))
            biases = tf.get_variable('biases', shape=[128], initializer=tf.truncated_normal_initializer(stddev=0.1))
            fc = tf.nn.relu(tf.matmul(reshape, weithts) + biases)


# losses
def losses(logits, label):
    # label 没有做one_hot转换的话,可以使用是sparse_softmax_cross_entropy_with_logits
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=label)
    loss = tf.reduce_mean(cross_entropy)
    return loss


# 优化器
def train_optm(loss, learning_rate):
    optimizer = tf.train.AdamOptimizer(learning_rate)
    global_step = tf.Variable(0, trainable=False)
    train_op = optimizer.minimize(loss, global_step)
    return train_op


'''
# 准确率
# 如果你设置的label是0或者1,但是你的logist是概率输出,怎么做准确率呢?
# argmax
# 推荐另外一种方法叫做:in_top_k(logist, labels, 1)
'''
def evaluation(logits, labels):
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.arg_max(logits, 1))), tf.arg_max(labels, 1))

