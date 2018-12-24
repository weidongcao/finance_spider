# -*- coding:utf-8 -*-
import string
from collections import namedtuple


def str_count(s):
    """找出字符串中的中英文、空格、数字、标点符号个数"""

    count_en = count_dg = count_sp = count_zh = count_pu = 0
    s_len = len(s)
    for c in s:
        if c in string.ascii_letters:
            count_en += 1
        elif c.isdigit():
            count_dg += 1
        elif c.isspace():
            count_sp += 1
        elif c.isalpha():
            count_zh += 1
        else:
            count_pu += 1
    total_chars = count_zh + count_en + count_sp + count_dg + count_pu
    if total_chars == s_len:
        return namedtuple('Count', ['total', 'zh', 'en', 'space', 'digit', 'punc'])(s_len, count_zh, count_en, count_sp, count_dg, count_pu)
    else:
        print('Something is wrong!')
        return None
    return None

