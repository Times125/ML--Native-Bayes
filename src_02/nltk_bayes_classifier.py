#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 利用朴素贝叶斯分类器对邮件进行分类
"""
from collections import Counter

import nltk
from nltk.corpus import *
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import *

__author__ = 'Lich'

"""
文本处理
"""


def text_parse(input_text):
    sentence = input_text.lower()
    special_tag = ['.', ',', '!', '#', '(', ')', '*', '`', ':', '?', '"']
    pattern = r""" (?x)(?:[A-Z]\.)+ 
                  | \d+(?:\.\d+)?%?\w+
                  | \w+(?:[-']\w+)*
                  | (?:[,.;'"?():-_`])"""

    word_list = regexp_tokenize(sentence, pattern)
    filter_word = [w for w in word_list if w not in stopwords.words('english') and w not in special_tag]  # 去停用词和特殊标点符号
    word_tag = nltk.pos_tag(filter_word)  # 词性标注，返回标记列表[('Codeine', 'NNP'), ('15mg', 'CD')]
    res_word_list = []
    for i in range(0, len(word_tag)):  # 去掉副词、介词、小品词、疑问词、代词、人称代词、所有格代名词等
        if word_tag[i][1] == 'TO' or word_tag[i][1] == 'RB' or word_tag[i][1] == 'RBR' \
                or word_tag[i][1] == 'RBRS' or word_tag[i][1] == 'UH' or word_tag[i][1] == 'WDT' \
                or word_tag[i][1] == 'WP' or word_tag[i][1] == 'WP$' or word_tag[i][1] == 'WRB' \
                or word_tag[i][1] == 'SYM' or word_tag[i][1] == 'RP' or word_tag[i][1] == 'PRP' \
                or word_tag[i][1] == 'PRP$' or word_tag[i][1] == 'CD':
            pass
        else:
            res_word_list.append(word_tag[i][0])
    return res_word_list


'''
提取文本特征，TF-IDF算法（这里利用词形还原（也可以利用词干提取））
'''


def get_features(input_matrix_data):
    input_matrix = input_matrix_data
    words_count_matrix = get_lemmatizer(input_matrix)
    res = calculate_tf(input_matrix, words_count_matrix)

    for i in range(0, 20):
        print words_count_matrix[i].items()


'''
计算词频
'''


def calculate_tf(word_matrix, words_count_matrix):
    res = []
    
    return res


'''
计算逆文档频率
'''


def calculate_idf():
    pass


''''
词形还原
'''


def get_lemmatizer(input_matrix):
    words_count = []
    lemmatizer = WordNetLemmatizer()  # 词形还原
    for lst in input_matrix:
        lemmated = []
        for item in lst:
            lemmated.append(lemmatizer.lemmatize(item))  # 词形还原
        words_count.append(Counter(lemmated))  # 计算每个词在其文本中出现的次数
    return words_count


'''
词干提取
'''


def get_stem(input_matrix):
    words_count = []
    stemmer = PorterStemmer()  # 词干提取
    for lst in input_matrix:
        stemmed = []
        for item in lst:
            stemmed.append(stemmer.stem(item))  # 词干提取
        words_count.append(Counter(stemmed))  # 计算每个词在其文本中出现的次数


'''
训练分类器
'''


def train_native_bayes_classifier():
    pass
