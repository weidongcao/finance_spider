import tensorflow as tf
class TextCNN(object):
    def __init__(self, sequence_length, num_classes,vocab_size, embedding_size,filter_sizes, num_filters):
        # sequence_length句子的长度
        # num_classes分类类别数
        # vocab_size 词典大小
        # embedding_size词向量大小
        # filter-sizes卷积核大小的list
        # num_filters 每个卷积核的个数
        self.input_x = tf.placeholder(tf.int32, [None, sequence_length])
        self.input_y = tf.placeholder(tf.float32, [None, num_classes])
        self.drop_out = tf.placeholder(tf.float32)

        # 词向量化
        with tf.name_scope('embedding'):
            self.W = tf.Variable(tf.random_uniform([vocab_size, embedding_size]))
            self.embedded_chars = tf.nn.embedding_lookup(self.W, self.input_x)

            # 根据input_x的下标一一对应去W中取对应索引的值作为当前的向量
            pooled_outputs = []
            for i, filter_size in enumerate(filter_sizes):
                with tf.name_scope('conv_maxpool-%s'%filter_size):
                    filter_shape = [filter_size, embedding_size, 1, num_filters]
                    # 高斯初始化卷积核
                    W = tf.Variable(tf.truncated_normal(filter_shape, stddev=01.), name='W')
                    b = tf.Variable(tf.constant(0.1), [num_filters], name='b')
                    conv = tf.nn.conv2d(self.embedded_chars, W, strides=[1, 1, 1, 1], padding='VALID')
                    h = tf.nn.relu(tf.nn.bias_add(conv, b))
                    pooled = tf.nn.max_pool(h, ksize=[1, sequence_length - filter_size + 1, 1, 1])
                    pooled_outputs.append(pooled)
            num_filters_total = num_filters * len(filter_sizes)
            self.h_pool = tf.concat(pooled_outputs, 3)
            self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])

            # 全链接
            # dropout
            with tf.name_scope('dropout'):
                self.h_drop = tf.nn.dropout(self.h_pool_flat, self.drop_out)
            with tf.name_scope('out'):
                W = tf.get_variable('W', shape=[num_filters_total, num_classes])
                b = tf.get_variable('b', shape=[num_classes])
                self.scores = tf.nn.xw_plus_b(self.h_drop, W, b)
                self.predictions = tf.argmax(tf.nn.softmax(self.scores), 1)
            with tf.name_scope('loss'):
                losses = tf.nn.softmax_cross_entropy_with_logits(self.scores, self.input_y)
                self.loss = tf.reduce_mean(losses)

            with tf.name_scope('accuarcy'):
                corrent_predictions = tf.equal()