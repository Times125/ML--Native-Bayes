#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 
"""
import nltk
from nltk.tokenize import *
from nltk.corpus import *

__author__ = 'Lich'

'''
分词，去除停用词，词性分析去动词、助词等
'''


def text_parse(input_text):
    sentence = input_text
    special_tag = ['.', ',', '!', '#', '(', ')', '*', '`', ':','?']
    pattern = r""" (?x)(?:[A-Z]\.)+ 
                  | \d+(?:\.\d+)?%?\w+
                  | \w+(?:[-']\w+)*
                  | (?:[,.;'"?():-_`])"""

    word_list = regexp_tokenize(sentence, pattern)
    filter_word = [w for w in word_list if w not in stopwords.words('english') and w not in special_tag]  # 去停用词和特殊标点符号

    word_tag = nltk.pos_tag(filter_word)  # 词性标注，返回标记列表[('Codeine', 'NNP'), ('15mg', 'CD')]
    res_word_list = []
    for i in range(len(word_tag)):
        if word_tag[i][1] == 'VB' or word_tag[i][1] == 'VBP' or word_tag[i][1] == 'VBN'\
                or word_tag[i][1] == 'TO' or word_tag[i][1] == 'PRP':
            pass
        else:
            res_word_list.append(word_tag[i][0])
    print word_tag
    print res_word_list
