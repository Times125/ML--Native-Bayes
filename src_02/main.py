#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本总数为30，其中环境类、政治类、经济类文本各10份
"""
__author__ = 'Lich'

from nltk_bayes_classifier import *


def main():
    post_list = []
    vocab_set = set([])
    dirs = ['env']  # , 'eco', 'pol']
    for name in dirs:
        for i in range(1, 11):
            res_word_list, doc_set = text_parse(
                open(u'C:\\Users\\Lich\\Desktop\\test\\' + name + u'\\%d.txt' % i).read().decode('utf-8'))
            post_list.append(res_word_list)
            vocab_set = vocab_set | doc_set
    print len(list(vocab_set))
    get_doc_features(post_list, list(vocab_set))


if __name__ == '__main__':
    main()
