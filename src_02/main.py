#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本总数为30，其中环境类、政治类、经济类文本各10份
"""
__author__ = 'Lich'

import time

from nltk_bayes_classifier import *
from text_processing import *


def main():
    start_time = time.time()
    features = get_class_features()  # 这是自己建立的语料库
    mid_time2 = time.time()
    dirs = ['env', 'eco', 'pol']
    vocab_set = set([])
    post_list = []
    '''
    # 程序耗时部分1
    for dir_name in dirs:
        for i in range(7, 11):
            res_word_list, doc_set = text_parse(
                open(r'G:\Repositories\ML--Native-Bayes\test\\' + dir_name + r'\%d.txt' % i).read().decode(
                    'utf-8'))  # 读取测试文本
            post_list.append((res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
            vocab_set = vocab_set | doc_set
    mid_time = time.time()
    print 'read test files cost total time %.4f seconds' % (mid_time - mid_time2)
    native_bayes_classifier(features, post_list, vocab_set)
    '''
    end_time = time.time()
    print 'method main() cost total time %.4f seconds' % (end_time - start_time)


if __name__ == '__main__':
    main()
    # import_data_from_csv2()