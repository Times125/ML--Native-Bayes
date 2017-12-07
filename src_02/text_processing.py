#! /usr/bin/env python
# encoding: utf-8

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 文本处理，构建自己的新闻语料库
"""

import Queue
import codecs
import time
import os

from nltk import pos_tag
from nltk.corpus import wordnet as wn
from collections import Counter
from nltk.corpus import stopwords as stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import *
from numpy import *
import threading
import sys

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Lich'
'''
stopwords.__class__
WordNetLemmatizer.__class__
stopwords.ensure_loaded()
wn.ensure_loaded()
'''
'''
文本处理，包括分词，去停用词、去无用词、词形还原等
'''

def text_parse(input_text):
    sentence = input_text.lower()
    lemmatizer = WordNetLemmatizer()  # 词形还原
    vocab_set = set([])  # 记录所有出现的单词
    special_tag = ['.', ',', '!', '#', '(', ')', '*', '`', ':', '?', '"', '‘', '’', '“', '”', '！', '：', '^', '/']
    pattern = r""" (?x)(?:[A-Z]\.)+ 
                  | \d+(?:\.\d+)?%?\w+
                  | \w+(?:[-']\w+)*
                  | (?:[,.;'"?():-_`])"""
    tag_list = ['TO', 'RB', 'RBR', 'RBRS', 'UH', 'WDT', 'WP', 'WP$', 'WRB', 'SYM', 'RP', 'PRP', 'PRP$', 'CD']
    word_list = regexp_tokenize(sentence, pattern)
    filter_word = [w for w in word_list if w not in stopwords.words('english') and w not in special_tag]  # 去停用词和特殊标点符号
    word_tag = pos_tag(filter_word)  # 词性标注，返回标记列表[('Codeine', 'NNP'), ('15mg', 'CD')]
    res_word_list = []
    for i in range(0, len(word_tag)):  # 去掉副词、介词、小品词、疑问词、代词、人称代词、所有格代名词等
        if word_tag[i][1] in tag_list:
            pass
        else:
            word = lemmatizer.lemmatize(word_tag[i][0])
            res_word_list.append(word)
            vocab_set.add(word)
    return res_word_list, vocab_set


'''
从挑选的各类文档中提取出能够代表各类文档的特征集合，输入的各类文档数目越多，特征集合越完善，分类效果越好；
提取文本特征，TF-IDF算法（这里利用词形还原（也可以利用词干提取））
返回每篇文章的特征值集合[['a','b'],['c','d'],...,['y',['z']]]
'''


def get_doc_features(input_matrix_data, vocab_set, threshold=0.008):

    start_time = time.time()
    input_matrix = input_matrix_data
    doc_nums = len(input_matrix)  # 输入的文档总数
    words_tf, words_count_matrix = calculate_tf(input_matrix)  # 计算词频
    n_contain_dict = calculate_d(words_count_matrix, vocab_set)  # 计算包含某单词a 的文档数目
    words_idf = calculate_idf(doc_nums, n_contain_dict)  # 计算逆文档
    words_tf_idf, sorted_tf_idf = calculate_tf_idf(doc_nums, words_tf, words_idf)  # 计算一篇文档中单词的tf-idf值

    # 取特征：设置阈值,取tf-idf值大于0.008,这个阈值需要根据分类结果进行调整
    doc_features = []
    for i in range(0, len(sorted_tf_idf)):
        tmp = []
        for tuple_w in sorted_tf_idf[i]:
            if tuple_w[1] >= threshold:
                tmp.append(tuple_w[0])
        doc_features.append(tmp)
        del tmp
    end_time = time.time()
    print 'method get_doc_features() cost total time %0.4f seconds' % (end_time - start_time)
    return doc_features


'''
计算TF-IDF
'''


def calculate_tf_idf(doc_nums, words_tf, words_idf):
    res = []
    sorted_res = []
    for i in range(0, doc_nums):
        tf_idf_dict = {}
        for word in words_tf[i]:
            tf_idf_dict[word] = (words_tf[i][word] * words_idf[word])
        res.append(tf_idf_dict)
        sorted_res.append(sorted(tf_idf_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True))  # 按照tf-idf 值从大到小进行排序
        del tf_idf_dict
    return res, sorted_res


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


def calculate_tf(input_matrix):
    res_list = []
    words_count = []
    for lst in input_matrix:
        words_count.append(Counter(lst))

    for lst in words_count:
        tf_dict = {}
        for word in lst.keys():
            tf_dict[word] = lst[word] / float(sum(lst.values()))  # 计算词频
        res_list.append(tf_dict)
        del tf_dict
    return res_list, words_count


'''
计算逆文档频率
'''


def calculate_idf(doc_nums, n_contain_dict):
    idf_dict = {}
    for word in n_contain_dict.keys():
        idf_dict[word] = log(doc_nums / (n_contain_dict[word]+1))
    return idf_dict


'''
返回每个类型的特征集合，建立自己的语料库
'''


def get_class_features():
    start_time = time.time()
    win_path = r'G:\Repositories\ML--Native-Bayes\material\\'
    mac_path = r'/Users/lch/Desktop/pycharm/Bayes/material/'
    files_list = []
    post_list = []
    total_vocab_set = set([])
    dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
    features = []
    categories = []
    env = []
    eco = []
    pol = []
    cul = []
    ene = []
    tec = []
    sec = []
    q = Queue.Queue()
    # 多线程读文件
    for item in dirs:
        file_path = win_path + item
        t = threading.Thread(target=read_file, args=(file_path, item, q))
        t.start()
    t.join()  # 线程同步
    while not q.empty():
        files_list.append(q.get(True))  # 获取读文件的内容

    t_time = time.time()
    for tup in files_list:
        if tup[1] == dirs[0]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[1]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[2]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[3]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[4]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[5]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])
        elif tup[1] == dirs[6]:
            for per_doc in tup[0]:
                res_word_list, doc_set = text_parse(per_doc[0])
                post_list.append(res_word_list)
                total_vocab_set = total_vocab_set | doc_set
                categories.append(tup[1])

        t_time_end = time.time()
    print '线程耗时%.4f 秒' % (t_time_end - t_time)
    print '文本去除停用词、词形还原后还剩余', len(list(total_vocab_set)), '个不重复单词。'
    docs_features = get_doc_features(post_list, total_vocab_set, 0.008)

    for i in range(0, len(categories)):
        if categories[i] == 'culture':
            cul.extend(docs_features[i])
        elif categories[i] == 'economy':
            eco.extend(docs_features[i])
        elif categories[i] == 'energy':
            ene.extend(docs_features[i])
        elif categories[i] == 'environment':
            env.extend(docs_features[i])
        elif categories[i] == 'political':
            pol.extend(docs_features[i])
        elif categories[i] == 'security':
            sec.extend(docs_features[i])
        elif categories[i] == 'technology':
            tec.extend(docs_features[i])
        else:
            pass
    features.append((env, 'environment'))
    features.append((eco, 'economy'))
    features.append((pol, 'political'))
    features.append((cul, 'culture'))
    features.append((sec, 'security'))
    features.append((tec, 'technology'))
    features.append((ene, 'energy'))

    end_time = time.time()
    print 'method get_class_features() cost total time %0.4f seconds' % (end_time - start_time)
    return features


'''
读取某一类文件夹的所有文件
'''


def read_file(path_name, category, queue):
    path_dir = os.listdir(path_name)
    content_list = []
    for fn in path_dir:
        f = codecs.open(os.path.join(path_name, fn), 'rb', 'utf-8')
        txt = f.read().decode('utf-8')
        f.close()
        content_list.append(list([txt]))
    queue.put((content_list, category))  # 包含了： （每篇新闻处理后的结果[[],[]]，这一类新闻的类别str）
