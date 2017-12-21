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
import langid
from collections import Counter
from threading import Thread
from config import *
from nltk import pos_tag, pos_tag_sents
from nltk.corpus import stopwords as stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import *
from numpy import *
from numpy.ma import log
from multiprocessing import Pool, Manager
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
    language = langid.classify(sentence)[0]
    lemmatizer = WordNetLemmatizer()  # 词形还原
    vocab_set = set([])  # 记录所有出现的单词
    special_tag = set(['.', ',', '!', '#', '(', ')', '*', '`', ':', '?', '"', '‘', '’', '“', '”', '！', '：', '^', '/',']', '['])
    pattern = r""" (?x)(?:[a-z]\.)+ 
                  | \d+(?:\.\d+)?%?\w+
                  | \w+(?:[-']\w+)*
                  | (?:[,.;'"?():-_`])"""

    tag_list = set(['TO', 'RB', 'RBR', 'RBRS', 'UH', 'WDT', 'WP', 'WP$', 'WRB', 'SYM', 'RP', 'PRP', 'PRP$', 'CD', 'POS', ':'])
    word_list = regexp_tokenize(sentence, pattern)
    if language == 'en':
        filter_word = [w for w in word_list if w not in stopwords.words('english') and w not in special_tag]  # 去停用词和特殊标点符号
    if language == 'fr':
        filter_word = [w for w in word_list if w not in stopwords.words('french') and w not in special_tag]  # 去停用词和特殊标点符号
    else:
        return [], set([])
    word_tag = pos_tag(filter_word, tagset=None, lang=language)  # 词性标注，返回标记列表[('Codeine', 'NNP'), ('15mg', 'CD')
    res_word_list = []
    for i in range(0, len(word_tag)):  # 去掉副词、介词、小品词、疑问词、代词、人称代词、所有格代名词等
        if word_tag[i][1] in tag_list:
            continue
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


def get_doc_features(input_matrix_data, vocab_set, thresholds=0.008):
    start_time = time.time()
    input_matrix = input_matrix_data
    doc_nums = len(input_matrix)  # 输入的文档总数
    words_tf, words_count_matrix = calculate_tf(input_matrix)  # 计算词频
    n_contain_dict = calculate_d(words_count_matrix, vocab_set)  # 计算包含某单词a 的文档数目
    words_idf = calculate_idf(doc_nums, n_contain_dict)  # 计算逆文档
    words_tf_idf, sorted_tf_idf = calculate_tf_idf(doc_nums, words_tf, words_idf)  # 计算一篇文档中单词的tf-idf值

    print 'method get_doc_features() calculate TF-IDF cost total time %0.4f seconds' % (time.time() - start_time)  # 77秒
    # 取特征：设置阈值,取tf-idf值大于0.01,这个阈值需要根据分类结果进行调整
    doc_features = []
    for i in range(0, len(sorted_tf_idf)):
        tmp = []  # 不能保证特征里面没有重复的值
        for tuple_w in sorted_tf_idf[i]:
            if tuple_w[1] >= thresholds:
                tmp.append(tuple_w[0])
        doc_features.append(tmp)
        del tmp
    end_time = time.time()
    print 'method get_doc_features() cost total time %0.4f seconds' % (end_time - start_time)  # 77秒
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
        idf_dict[word] = log(doc_nums / (n_contain_dict[word] + 1))
    return idf_dict


'''
返回每个类型的特征集合，建立自己的语料库
'''

def get_class_features():
    start_time = time.time()
    files_list = []
    post_list = []
    threads = []
    total_vocab_set = set([])
    features = []
    m_categories = []
    # 'social_fr', 'political_fr', 'international_fr', 'economy_fr'
    clas = []

    for i in range(len(categories)):
        clas.append([])

    qt = Queue.Queue()  # 线程用的队列
    pool = Pool(len(dirs))  # 开启n个进程
    manager = Manager()
    qp = manager.Queue()  # 进程用的队列
    # 多线程读文件
    for item in dirs:
        file_path = os.path.join(material_path, item)
        t = Thread(target=read_file, args=(file_path, item, qt))
        threads.append(t)
        t.start()
        t.setName(item+' thread')
    for t in threads:
        t.join()  # 线程同步
    print u'队列长度', qt.qsize()
    while not qt.empty():
        files_list.append(qt.get(True))  # 获取读文件的内容

    # 这里可以开多个线程来处理
    t_time = time.time()
    print 'Parent process ID %d' % os.getpid()
    for tup in files_list:  # [（[[doc1],[doc2]]，cat1）,([[doc1],[doc2]]，cat2）,...,([[doc1],[doc2]]，cat7）]
        if tup[1] == 'international_fr':
            pool.apply_async(deal_doc, (tup[0], tup[1], qp))
    pool.close()  # 关闭子进程
    pool.join()  # 等待进程同步
    print 'size------', qp.empty()
    a = 0
    while not qp.empty():
        res = qp.get(True)
        post_list.extend(res[0])
        total_vocab_set = total_vocab_set | res[1]
        m_categories.extend(res[2])
        print a
        a += 1
    t_time_end = time.time()
    print u'进程耗时%.4f 秒' % (t_time_end - t_time) # 453秒
    print u'文本去除停用词、词形还原后还剩余', len(list(total_vocab_set)), u'个不重复单词。'
    docs_features = get_doc_features(post_list, total_vocab_set, threshold)  # 获得每篇文档的特征[[],[],..,[]]

    tmp_dict = {}
    for i in range(0,len(m_categories)):
        for j in range(0,len(categories)):
            if categories[j] == m_categories[i]:
                clas[j].extend(docs_features[i])
                ck = categories[j]
                tmp_dict[ck] = clas[j]

    print len(m_categories), ' - ', len(docs_features), ' - ', len(categories)
    print tmp_dict.keys()

    for cat in categories:
        features.append((list(set(tmp_dict[cat])), cat))
    """
    env = []
    eco = []
    pol = []
    cul = []
    ene = []
    tec = []
    sec = []
    fr_soc = []
    fr_pol = []
    fr_int = []
    fr_eco = []
    for i in range(0, len(m_categories)):
        if m_categories[i] == 'culture':
            cul.extend(docs_features[i])
        elif m_categories[i] == 'economy':
            eco.extend(docs_features[i])
        elif m_categories[i] == 'energy':
            ene.extend(docs_features[i])
        elif m_categories[i] == 'environment':
            env.extend(docs_features[i])
        elif m_categories[i] == 'political':
            pol.extend(docs_features[i])
        elif m_categories[i] == 'security':
            sec.extend(docs_features[i])
        elif m_categories[i] == 'technology':
            tec.extend(docs_features[i])
    features.append((list(set(env)), 'environment'))
    features.append((list(set(eco)), 'economy'))
    features.append((list(set(pol)), 'political'))
    features.append((list(set(cul)), 'culture'))
    features.append((list(set(sec)), 'security'))
    features.append((list(set(tec)), 'technology'))
    features.append((list(set(ene)), 'energy'))
    """
    end_time = time.time()
    print 'method get_class_features() cost total time %0.4f seconds' % (end_time - start_time)  # 530秒
    return features


'''
处理一个文档，多线程用的
'''
def deal_doc(n_list, category, qp):

    p_list = []
    p_categories = []
    p_vocab_set = set([])
    print 'sub process ID %d' % os.getpid()
    for per_doc in n_list:
        res_word_list, doc_set = text_parse(per_doc[0])
        if res_word_list is None or doc_set is None:
            continue
        p_list.append(res_word_list)
        p_vocab_set = p_vocab_set | doc_set
        p_categories.append(category)
    res = (p_list, p_vocab_set, p_categories)
    print res,'cccccccccccc'
    qp.put(res, True)


'''
读取某一类文件夹的一半文件
'''
def read_file(path_name, category, queue):
    path_dir = os.listdir(path_name)
    files_num = len(path_dir)
    content_list = []
    for fn in range(files_num/40):
        file_name = os.path.join(path_name, r'%d.txt' % fn)
        with codecs.open(file_name, 'rb', 'utf-8') as reader:
            txt = reader.read().decode('utf-8')
            content_list.append(list([txt]))
    res = (content_list, category)
    queue.put(res)  # 包含了： （每篇新闻处理后的结果[[],[]]，这一类新闻的类别str）
