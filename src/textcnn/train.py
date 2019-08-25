import tensorflow as tf
import data_helper
import TextCNNModel
import numpy as np
from tensorflow.contrib import learn

positive_data_dir = 'data/rt-polaritydata/rt-polarity.pos'
negative_data_dir = 'data/rt-polaritydata/rt-polarity.pos'
x_text, y = data_helper.load_data_and_label(positive_data_dir, negative_data_dir)

# 找到数据集中最长的一条记录
max_document_length = max([len(x.split(" ")) for x in x_text])
# 传入最大的长度,默认我们填充0
vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)
x = np.array(list(vocab_processor.fit_transform(x_text)))

shuffle_indices = np.random.permutation(np.arange(len(y)))
x_shffled = x[shuffle_indices]
y_shffled = y[shuffle_indices]

# 生成字典
voc = vocab_processor.vocabulary_
cnn = TextCNNModel.TextCNN(
    sequence_length=x_shffled.shape[1],
    num_classes=y_shffled.shape[1],
    vocab_size=len(voc),
    embedding_size=128,
    filter_sizes=[3,4,5],
    num_filters=128
)

# 照常训练
