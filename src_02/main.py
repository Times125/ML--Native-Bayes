#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本包括：环境类、政治类、经济类、文化类、技术类、安全类和能源类文本
"""
import getopt
import time
import sys
import os
import codecs
import re
import socket
import pickle
from openpyxl import load_workbook
from config import *
from nltk_bayes_classifier import import_features_from_lib, get_model
from nltk_bayes_classifier import import_data_from_excel, train_native_bayes_classifier
from export_data import build_features_lib
from text_processing import text_parse
from multiprocessing import Pool, Manager,Queue

__author__ = 'Lich'


def main():
    classifier = get_model()
    with open(os.path.join(model_path, 'all_words.pkl'), 'rb') as f:
        all_words = pickle.load(f)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9898))
    s.listen(10)
    while True:
        sock, addr = s.accept()
        data = sock.recv(102400)
        data = data.decode('utf-8').encode('utf-8')
        if data is 'auto':
            import_data_from_excel()
            build_features_lib()
            import_features_from_lib()  # 这是自己建立的语料库
            train()
            sock.send("complete auto!")
            continue
        res = classify_text(data, classifier, all_words)
        sock.send(res)


def classify_text(txt, classifier, all_words):
    res_word_list, v = text_parse(txt)
    wait_for_class = {}
    for item in res_word_list:
        wait_for_class['contains(%s)' % item] = (item in all_words)
    res = classifier.classify(wait_for_class)
    return res


def train():
    start_time = time.time()
    with open(os.path.join(model_path, 'features.pkl'), 'rb') as f:
        features = pickle.load(f)
    mid_time2 = time.time()
    vocab_set = set([])
    post_list = []

    man = Manager()
    queue_pool = man.Queue()
    pool_t = Pool(len(dirs))  # 开n个进程

    print 'Parent process ID %d' % os.getpid()
    for dir_name in dirs:
        pool_t.apply_async(deal_train_doc, (dir_name, queue_pool,))
    pool_t.close()
    pool_t.join()

    print queue_pool.empty()
    while not queue_pool.empty():
        res = queue_pool.get(True)  # (p_post_list, p_vocab_set)
        for lst in res[0]:
            post_list.append(lst)
        vocab_set = vocab_set | res[1]

    mid_time = time.time()
    print 'read test files cost total time %.4f seconds' % (mid_time - mid_time2)  # 847秒 / 419s
    train_native_bayes_classifier(features, post_list, vocab_set)
    end_time = time.time()
    print 'method train() cost total time %.4f seconds' % (end_time - start_time)  #

def deal_train_doc(dir_name, queue_pool):
    import os
    p_post_list = []
    p_vocab_set = set([])
    fp = os.path.join(material_path, dir_name)
    files_num = len(os.listdir(fp))  # 一个类目录下文件数量
    print dir_name, u'此目录下共%d个txt文件' % files_num, 'deal_train_doc subprocess id %d' % os.getpid()
    for i in range(files_num / 2, files_num):
        with codecs.open(os.path.join(fp, r'%d.txt' % i), 'rb', 'utf-8') as reader:
            txt = reader.read()  # .decode('utf-8')
            p_res_word_list, p_doc_set = text_parse(txt)  # 读取测试文本
            p_post_list.append((p_res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
            p_vocab_set = p_vocab_set | p_doc_set
    print len(p_post_list), dir_name
    queue_pool.put((p_post_list, p_vocab_set))

'''
创建程序必要的文件目录
'''

def check_dirs():
    f_path = os.path.join(feature_path)
    t_path = os.path.join(test_path)
    mod_path = os.path.join(model_path)

    for dir_name in verifies:
        v_path = os.path.join(verify_path, dir_name)
        if not os.path.exists(v_path):
            os.makedirs(v_path)

    if not os.path.exists(mod_path):
        os.makedirs(mod_path)

    for dir_name in dirs:
        m_path = os.path.join(material_path, dir_name)
        if not os.path.exists(m_path):
            os.makedirs(m_path)
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        if not os.path.exists(t_path):
            os.makedirs(t_path)

def tests():
    classifier = get_model()
    with open(os.path.join(model_path, 'all_words.pkl'), 'rb') as f:
        all_words = pickle.load(f)
    for dir_name in verifies:
        wb = load_workbook(os.path.join(verify_path, dir_name + r'.xlsx'))
        sheet = wb.get_sheet_by_name("sheet1")
        tmp_path = os.path.join(verify_path, dir_name)
        a = 0
        for row in sheet['A']:
            file_name = os.path.join(tmp_path, str(a) + r'.txt')
            txt = str(row.value).decode('ISO-8859-15').encode('utf-8')
            if dir_name not in fr_categories:
                txt = re.sub(r'[^\x00-\x7F]+', '', txt)  # 去除所有非英语字符
            else:
                txt = re.sub(r'[^\x00-\xFF]+', '', txt)  # 去除所有非法语字符
            if not txt or len(txt) <= 150:  # 舍弃过短的文章
                continue
            with codecs.open(file_name, 'wb', 'utf-8', errors='ignore') as writer:
                writer.write(txt)
                a += 1
    total_num = 0
    uncorrected = 0
    for dir_name in verifies:
        file_path = os.path.join(verify_path, dir_name)
        file_num = len(os.listdir(file_path))
        total_num += file_num
        b = 0
        for i in range(file_num):
            fn = os.path.join(file_path, str(b) + r'.txt')
            with codecs.open(fn, 'rb', 'utf-8') as reader:
                txt = reader.read().decode('utf-8')
            res = classify_text(txt, classifier, all_words)
            if res != dir_name:
                uncorrected += 1
                print dir_name, ":", b, '.txt'
            b += 1
    print total_num, '  ', uncorrected
    print 'nb_classifier accuracy is : %.5f' % (1 - (uncorrected / float(total_num)))


if __name__ == '__main__':
    check_dirs()
    # main()  # 运行程序
    # import_data_from_excel()
    # build_features_lib()
    # import_features_from_lib()
    train()
    # tests()