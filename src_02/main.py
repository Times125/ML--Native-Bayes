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
    a = 0
    dirs = ['env', 'eco', 'pol']
    for name in dirs:
        for i in range(1, 11):
            res_word_list, doc_set = text_parse(
                open(u'/Users/lch/Desktop/pycharm/Bayes/test/' + name + u'/%d.txt' % i).read().decode('utf-8'))
            post_list.append(res_word_list)
            a += len(doc_set)
            vocab_set = vocab_set | doc_set
    print '文本去除停用词、词形还原后还剩余', len(list(vocab_set)), '个不重复单词。', '\n文本去除停用词后所有文本共含有', a, '个单词'
    doc_features = get_doc_features(post_list, vocab_set)
    for i in range(0, len(doc_features)):
        print doc_features[i], '\n'


if __name__ == '__main__':
    main()
