#! /usr/bin/env python
# encoding: utf-8

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 利用朴素贝叶斯分类器对新闻文本进行分类
"""
from collections import Counter

import nltk
from nltk.corpus import *
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import *
from numpy import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Lich'

"""
文本处理
"""


def text_parse(input_text):
    sentence = input_text.lower()
    vocab_set = set([])  # 记录所有出现的单词
    special_tag = ['.', ',', '!', '#', '(', ')', '*', '`', ':', '?', '"', '‘', '’']
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
            vocab_set.add(word_tag[i][0])
    return res_word_list, vocab_set


'''
提取文本特征，TF-IDF算法（这里利用词形还原（也可以利用词干提取））
返回每篇文章的特征值集合[['a','b'],['c','d'],...,['y',['z']]]
'''


def get_doc_features(input_matrix_data, vocab_set):
    input_matrix = input_matrix_data
    words_count_matrix = get_lemmatizer(input_matrix)
    n_contain_dict = calculate_d(input_matrix, vocab_set)
    doc_nums = len(input_matrix)  # 输入的文档总数
    words_tf = calculate_tf(words_count_matrix)
    words_idf = calculate_idf(doc_nums, n_contain_dict)

    print  words_tf
    print('\n\n')
    print words_idf


'''
计算包含某单词a 的文档数目
'''


def calculate_d(words_count_matrix, vocab_set):
    n_contain_dict = {}  # 包含此单词的文档数目
    for word in vocab_set:
        n = sum(1 for lst in words_count_matrix if word in lst)
        n_contain_dict[word] = n
    return n_contain_dict


'''
计算词频,一个单词在某个文档A中出现的频率
'''


def calculate_tf(words_count_matrix):
    res_list = []
    for lst in words_count_matrix:
        tf_dict = {}
        for word in lst.keys():
            tf_dict[word] = lst[word] / float(sum(lst.values()))  # 计算词频
        res_list.append(tf_dict)
        del tf_dict
    return res_list


'''
计算逆文档频率
'''


def calculate_idf(doc_nums, n_contain_dict):
    idf_dict = {}
    for word in n_contain_dict.keys():
        idf_dict[word] = log(doc_nums / n_contain_dict[word])
    return idf_dict


''''
词形还原
'''


def get_lemmatizer(input_matrix):
    words_count = []
    lemmated = []
    lemmatizer = WordNetLemmatizer()  # 词形还原
    for lst in input_matrix:
        for item in lst:
            lemmated.append(lemmatizer.lemmatize(item))  # 词形还原
        words_count.append(Counter(lemmated))  # 计算每个词在其文本中出现的次数
        del lemmated[:]
    return words_count


'''
词干提取
'''


def get_stem(input_matrix):
    words_count = []
    stemmed = []
    stemmer = PorterStemmer()  # 词干提取
    for lst in input_matrix:
        for item in lst:
            stemmed.append(stemmer.stem(item))  # 词干提取
        words_count.append(Counter(stemmed))  # 计算每个词在其文本中出现的次数
        del stemmed[:]
    return words_count


'''
训练分类器
'''


def train_native_bayes_classifier():
    pass
