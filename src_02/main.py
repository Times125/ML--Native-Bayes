#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本总数为30，其中环境类、政治类、经济类文本各10份
"""
__author__ = 'Lich'

from import_data import import_features_from_lib
from nltk_bayes_classifier import *
from text_processing import *


def main():
    start_time = time.time()
    features = import_features_from_lib()  # 这是自己建立的语料库
    mid_time2 = time.time()
    dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
    vocab_set = set([])
    post_list = []

    # 程序耗时部分1
    for dir_name in dirs:
        for i in range(0, 40):
            res_word_list, doc_set = text_parse(
                open(r'G:\Repositories\ML--Native-Bayes\material\\' + dir_name + r'\%d.txt' % i).read().decode(
                    'utf-8'))  # 读取测试文本
            post_list.append((res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
            vocab_set = vocab_set | doc_set
    mid_time = time.time()
    print 'read test files cost total time %.4f seconds' % (mid_time - mid_time2)
    native_bayes_classifier(features, post_list, vocab_set)

    end_time = time.time()
    print 'method main() cost total time %.4f seconds' % (end_time - start_time)


def tests():
    train = [({'a': 1, 'b': 0, 'c': 1}, 'y'),
             ({'a': 1, 'b': 0, 'c': 0}, 'y'),
             ({'a': 1, 'b': 1, 'c': 1}, 'x'),
             ({'a': 1, 'b': 1, 'c': 0}, 'x'),
             ({'a': 1, 'b': 1, 'c': 1}, 'x'),
             ({'a': 0, 'b': 0, 'c': 1}, 'y')]
    test = [({'a': 1, 'b': 0, 'c': 1}, 'y'),
            ({'a': 0, 'b': 0, 'c': 1}, 'y'),
            ({'a': 1, 'b': 0, 'c': 0}, 'y'),
            ({'a': 1, 'b': 1, 'c': 0}, 'x'),
            ({'a': 1, 'b': 1, 'c': 1}, 'x')]
    testp = [({'a': 1, 'b': 0, 'c': 1}),
            ({'a': 0, 'b': 0, 'c': 1}),
            ({'a': 1, 'b': 0, 'c': 0}),
            ({'a': 1, 'b': 1, 'c': 0}),
            ({'a': 1, 'b': 1, 'c': 1})]

    cla = nltk.classify.NaiveBayesClassifier.train(train)
    print cla.classify_many(testp)
    print 'test_accuracy is %.4f' % nltk.classify.accuracy(cla, test)


if __name__ == '__main__':
    main()
    # tests()
    # build_features_lib() # 建立特征语料库
    # import_data_from_csv()
