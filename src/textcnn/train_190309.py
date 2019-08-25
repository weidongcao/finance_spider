from load_data import *
from lstm_models import *

# 读取数据
poetrys = data_load()
# 构建字典
vocab, de_vocab = get_vocab(poetrys
                            )
# 转换文字
poetrys_vector = word2vec(vocab, poetrys)

# 初始化模型,执行训练
rnn_net = LstmRNN(batch_size=64, poetrys_vector=poetrys_vector, vocab=vocab, model_choice='lstm', hidden_size=256, num_layers=2, embdding_size=2)
