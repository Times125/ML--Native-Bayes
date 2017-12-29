#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/5 11:07
@Description: 将excel件转存到txt文件中
"""
from export_data import build_features_lib
from openpyxl import load_workbook
from config import *
import codecs
import re
import pickle
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'Lich'


def import_data_from_excel():
    print u'正在导入，请等待...'
    start_time = time.time()
    log_info = {}
    for dir_name in dirs:
        wb = load_workbook(os.path.join(test_path, dir_name + r'.xlsx'))
        sheet = wb.get_sheet_by_name("sheet1")
        tmp_path = os.path.join(material_path, dir_name)
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
        log_info[dir_name] = a
        end_time = time.time()
    for item in log_info:
        print item, u'类新闻共%d篇' % log_info[item]
    print u'excel文件导入TXT完成！ 一共耗时%.4f秒' % (end_time - start_time)


'''
从feature目录下的特征库读取特征
'''
def import_features_from_lib():
    features = []
    all_features_words = set([])
    for dir_name in dirs:
        file_name = os.path.join(feature_path, dir_name + '.txt')
        with codecs.open(file_name, 'rb') as reader:
            txt = reader.read().decode('ISO-8859-15').encode('utf-8')
            txt = re.sub(r'[^\x00-\xFF]+', '', txt)  # 去除所有非ASCII字符
            lst = txt.split(' ')
            # print dir_name, u"特征包含共%d个词" % len(lst)
            all_features_words = all_features_words | set(lst)
            features.append((lst, dir_name))  # [(lst1,cat1),(lst2,cat2),...,(lst7,cat7)]
    with open(os.path.join(model_path, 'all_words.pkl'), 'wb') as f:
        pickle.dump(all_features_words, f)
    with open(os.path.join(model_path, 'features.pkl'), 'wb') as f:
        pickle.dump(features, f)
    return features, all_features_words
