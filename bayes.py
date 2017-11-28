#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/22 11:42
@Description: 
"""
from numpy import *

def load_data_set():
    post_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]  # 1为侮辱性语料，0不是
    return post_list, class_vec


'''
传入语料集合
返回一个不重复的词条列表
'''
def create_vocab_list(data_set):
    vocab_set = set([])  # 创建一个空set
    for doc in data_set:
        vocab_set = vocab_set | set(doc)
    return list(vocab_set)


'''
传入不重复的词条列表和输入集
返回一个向量表示输入集的词项是否在训练的词条列表中
'''
def create_word_to_vec(vocab_list, input_set):
    vec = len(vocab_list) * [0]
    for word in input_set:
        if word in vocab_list:
            # vec[vocab_list.index(word)] = 1  # 词集模型
            vec[vocab_list.index(word)] += 1  # 词袋模型
        else:
            pass
    return vec

'''
传入训练集（已经转为向量），分类标签向量
朴素贝叶斯分类器训练
'''
def train_native_bayes(train_matrix, category):
    train_docs_num = len(train_matrix)
    words_num = len(train_matrix[0])
    p_bad = sum(category) / float(train_docs_num)  # 计算侮辱性语料的先验概率
    # 拉普拉斯平滑
    p0 = ones(words_num)  # 好的
    p1 = ones(words_num)  # 坏的
    p0_denom = 2.0
    p1_denom = 2.0
    for i in range(train_docs_num):
        if category[i] == 1:
            p1 += train_matrix[i]
            p1_denom += sum(train_matrix[i])
        else:
            p0 += train_matrix[i]
            p0_denom += sum(train_matrix[i])
    p0_vec = log(p0/p0_denom)
    p1_vec = log(p1/p1_denom)
    return p0_vec, p1_vec, p_bad

'''
分类器
'''
def classify_native_bayes(doc_vec, p0_vec, p1_vec, class_bad):
    p0 = sum(doc_vec * p0_vec) + log(class_bad)
    p1 = sum(doc_vec * p1_vec) + log(1 - class_bad)
    if p1 < p0:
        return 0
    else:
        return 1

