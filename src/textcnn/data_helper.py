import numpy as np
def load_data_and_label(postitive_data_file, negative_data_file):
    postitive_data = open(postitive_data_file, 'rb').read().decode('utf-8')
    negative_data = open(negative_data_file, 'rb').read().decode('utf-8')

    # 因为最后一行为空行,所以不取
    postitive_data = postitive_data.split('\n')[:-1]
    negative_data = negative_data.split('\n')[:-1]

    # 每一行的首位空字符去除
    postitive_data = [clean_str(s.strip()) for s in postitive_data]
    negative_data = [clean_str(s.strip()) for s in negative_data]

    x_text = postitive_data + negative_data

    postitive_label = [[0,1] for _ int postitive_data]
    negative_label = [[1,0] for _ in negative_data]
    y = np.concatenate([postitive_label, negative_label], 0)
    return  x_text, y

# 取出样本_batch
def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    data_size = len(data)

    num_batch_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffle_data = data[shuffle_indices]
        else:
            shuffle_data = data
        for batch_num in range(num_batch_epoch):
            start_index = batch_num * num_batch_epoch
