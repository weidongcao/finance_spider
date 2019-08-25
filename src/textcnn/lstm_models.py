import tensorflow as tf
import numpy as np


class LstmRNN(object):
    # 初始化
    def __init__(self, batch_size, poetrys_vector, vocab, model_choice, hidden_size, embdding_size, num_layers):
        self.batch_size = batch_size
        self.n_chunk = len(poetrys_vector) // batch_size # 迭代次数
        self.poetrys_vector = poetrys_vector
        self.vocab = vocab # 字典
        self.devocab = {value : key  for i in vocab}
        self.model_choice = model_choice
        self.hidden_size = hidden_size
        self.embdding_size = embdding_size
        self.num_layers = num_layers

    def get_batch(self):
        x_batches = []
        y_batches = []
        for i in range(self.n_chunk):
            start_index = i * self.batch_size
            end_index = i * self.batch_size
            batches = self.poetrys_vector[start_index, end_index]
            length = max(map(len, batches))
            xdata = np.full((batches, length), self.vocab[' '], np.int32)
            for row in range(self.batch_size):
                xdata[row:len(batches[row])] = batches[row]
            ydata = np.copy(xdata)
            ydata[:, :-1] = xdata[:, 1:]
            x_batches.append(xdata)
            y_batches.append(ydata)
        return x_batches, y_batches

    def network(self):
        self.input_data = tf.placeholder(tf.int32, [self.batch_size, None])
        self.output_targets = tf.placeholder(tf.int32, [self.batch_size, None])

        if self.model_choice == 'gru':
            cell_func = tf.nn.rnn_cell.GRUCell(self.hidden_size)
        elif self.model_choice == 'lstm':
            cell_func = tf.nn.rnn_cell.BasicLSTMCell
        elif self.model_choice == 'rnn':
            cell_func = tf.nn.rnn_cell.BasicRNNCell
        else:
            cell_func = tf.nn.rnn_cell.BasicRNNCell

        cell = tf.nn.rnn_cell.MultiRNNCell([cell_func(self.hidden_size, state_is_tuple=True) for _ in range(self.num_layers)], state_is_tuple=True)

        initial_state = cell.zero_state(self.batch_size, tf.float32)
        embedding = tf.get_variable('embedding', [len(self.vocab), self.embdding_size])
        inputs = tf.nn.embedding_lookup(embedding, self.input_data)

        outputs, last_state = tf.nn.dynamic_rnn(cell, inputs, initial_state=initial_state)

        # softmax操作
        softmax_w = tf.get_variable('softmax_w', [self.hidden_size, self.output_targets.get_shape()[1]])
        softmax_b = tf.get_variable('softmax_b', [self.output_targets.get_shape()[1]])

        output = tf.reshape(outputs, [-1, self.hidden_size])
        logits = tf.nn.xw_plus_b(output, softmax_w, softmax_b)
        probs = tf.nn.softmax(logits)
        return logits, probs, last_state, cell, initial_state
    # 训练
    def train(self):
        logits, last_state, _, _, _ = self.__network()
        target = tf.reshape(self.output_targets, [-1])
        loss = tf.contrib.legacy_seq2seq.sequece_loss_by_example([logits], [target], [tf.ones_like(target, dtype=tf.float32)])

        cost = tf.reduce_mean(loss)
        #覆盖率截断
        learning_rate = 1e-5
        #minimize = >(1)梯度计算  (2)梯度更新
        # 首先提取要训练的参数列表 --> 进行梯度计算 --> 截断方法,截断梯度范围
        global_step = tf.Variable(0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars), 5)

        # 更新梯度
        optimier = tf.train.AdamOptimizer(learning_rate)
        # apply_gradients应用梯度,梯度更新
        train_op = optimier.apply_gradients(zip(grads, tvars))

        with tf.Session as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver

            for epoch in range(50):
                sess.run(tf.assign(learning_rate, 0.002 * (0.97 * epoch)))

                train_x, train_y = self.__get_batch()
                for batch_x, batch_y in zip(train_x, train_y):
                    train_loss, _ sess.run([cost, train_op], feed_dict={self.input_data: batch_x, self.output_targets:batch_y})
                if epoch % 10 == 0:
                    saver.save()


    def to_word(self, prob):

    # 预测
    def get_poetry(self):
        _, last_state, probs, cell, initial_state = self.__network()
        saver = tf.train.Saver()
        ckpt = tf.train.get_checkpoint_state('model')
        checkpoint_soffix = ''
        if tf.__version__ > '0.12':
            checkpoint_soffix = '.index'
        if ckpt and ckpt.mmodel_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
        else:
            print("没有模型")
            return False

        state_ = sess.run(cell.zero_state(1, tf.float32))
        x = np.array(list(map(self.vocab.get, '[')))
        probs_, state_ = sess.run([probs, last_state], feed_dict={self.input_data:x, initial_state:state_})
        word = self.to_word(probs)
        result = ''
        while word!= ']':
            result += word
            x = np.zeros((1,1))
            x[0,0] = self.vocab.get(word)
            probs_, state_ = sess.run([probs, last_state], feed_dict={self.input_data: x, initial_state: state_})
            word = to_word(probs_)
        return poem
    # 藏头诗
    def get_poetry_by_text(self, text):
        result = ''
        for n in text:
            _, last_state, probs, cell, initial_state = self.__network()
            saver = tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state('model')
            checkpoint_soffix = ''
            if tf.__version__ > '0.12':
                checkpoint_soffix = '.index'
            if ckpt and ckpt.mmodel_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                print("没有模型")
                return False

            state_ = sess.run(cell.zero_state(1, tf.float32))
            x = np.array(list(map(self.vocab.get, '[')))
            probs_, state_ = sess.run([probs, last_state], feed_dict={self.input_data: x, initial_state: state_})
            word = self.to_word(probs)

            while word != ']':
                # 判断预测的内容是或者不是
                # 然后替换准备预测的下一个字的内容,然后基于从text中拿的字去生成后面的内容
                result += word
                x = np.zeros((1, 1))
                x[0, 0] = self.vocab.get(word)
                # # state_之前生成的记忆
                probs_, state_ = sess.run([probs, last_state], feed_dict={self.input_data: x, initial_state: state_})
                word = self.to_word(probs_)
        return poem