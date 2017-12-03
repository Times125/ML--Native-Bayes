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
    categories = []
    env = []
    eco = []
    pol = []
    for name in dirs:
        for i in range(1, 6):
            res_word_list, doc_set = text_parse(
                open(u'/Users/lch/Desktop/pycharm/Bayes/test/' + name + u'/%d.txt' % i).read().decode('utf-8'))
            post_list.append(res_word_list)
            vocab_set = vocab_set | doc_set
            categories.append(name)
            a += len(doc_set)
    print '文本去除停用词、词形还原后还剩余', len(list(vocab_set)), '个不重复单词。', '\n文本去除停用词后所有文本共含有', a, '个单词'

    train_docs_features = get_doc_features(post_list, vocab_set)
    features = []
    for i in range(0, len(train_docs_features)):
        if categories[i] == 'env':
            env.extend(train_docs_features[i])
        elif categories[i] == 'eco':
            eco.extend(train_docs_features[i])
        elif categories == 'pol':
            pol.extend(train_docs_features[i])

        features.append((train_docs_features[i], categories[i]))
        # print train_docs_features[i], '\n'
    print env
    # native_bayes_classifier(docs_features, vocab_set)


if __name__ == '__main__':
    main()
