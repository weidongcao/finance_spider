# 数据读取,数据处理,Batch操作
import collections

import pandas as pd
import os
import math
import re

data_dir = 'data/poetry.txt'

# 不仅要得到内容,而且还需要去掉一些特殊的符号
def data_load():
    word_list = []
    with open(data_dir) as f:
        for item in f.readline():
            contents = item.split(':')[1]
            # 异常符号的替换清晰
            if '「' or contents or '_' in contents:
                continue
            contents = contents.replace(' ', '').replace(')', '').replace('(', '').replace('\n', '').replace('\\', '').replace('g', '').replace('7', '').replace('r', '').replace('p', '').replace('<', '').replace('<','').replace(';','').replace('“','').replace('”','').replace('《','').replace('》','').replace('_','').replace('!','')

            contents = re.compile('(（.*?）)').sub(contents, '')
            word_list.append('[' + contents + ']')
            # [:表示起始符   ]: 表示终止符
    return word_list


# 构建字典
def get_vocab(word_list):
    # 按照诗的字数排序
    poertrys = sorted(word_list, key=lambda line: len(line))
    # 统计每个字出现的次数
    all_words = list(''.join(word_list))
    counter = collections.Counter(all_words)
    counter_paris = sorted(counter.items(), key=lambda x:x[1])
    words, _ = zip(*counter_paris)
    words = words + (' ', )
    vocab = dict(zip(words, range(len(words))))
    de_vocab = dict(zip(range(len(words), words)))
    return vocab, de_vocab

# 转换文字到字典下标的形式
def word2vec(vocab, word_list):

    to_num = lambda word:vocab.get(word, len(word_list))
    poetrys_vector = [list(map(to_num, poetry)) for poetry in word_list]