#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/5 11:07
@Description: 将csv文件转存到txt文件中
"""
import codecs
import csv
import sys
import time
from export_data import build_features_lib
import os
reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'Lich'

win_f_path = r'G:\Repositories\ML--Native-Bayes\features'
mac_f_path = r'/Users/lch/Desktop/pycharm/Bayes/features'
win_path = r'G:\Repositories\ML--Native-Bayes\material'
mac_path = r'/Users/lch/Desktop/pycharm/Bayes/material/'
dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
def import_data_from_csv():
    print '正在导入，请等待...'
    start_time = time.time()
    log_info = {}
    for dir_name in dirs:
        csv_reader = csv.reader(
            open(r'C:\Users\Lich\Desktop\material' + u'\\' + dir_name + u'\\' + dir_name + r'.csv', 'r'))
        a = 0
        for row in csv_reader:
            if len(row) == 0:
                pass
            else:
                f = codecs.open(win_path + u'\\' + dir_name + u'\\' + str(a) + r'.txt', 'w', 'utf-8', errors='ignore')
                try:
                    txt = str(row[0]).decode('gbk').encode('utf-8')
                except UnicodeDecodeError, e:
                    pass
                f.write(txt)
                f.close()
                a += 1
        log_info[dir_name] = a
    end_time = time.time()
    for item in log_info:
        print item, '类新闻共%d篇' % log_info[item]
    print 'CSV文件导入TXT完成！ 一共耗时%.4f秒' % (end_time - start_time)

'''
从特征库读取特征
'''
def import_features_from_lib():
    features = []
    if not os.path.exists(win_f_path):
        build_features_lib()
    else:
        for dir_name in dirs:
            f = codecs.open(os.path.join(win_f_path, dir_name + '.txt'), 'rb', 'utf-8')
            txt = f.read().decode('utf-8')
            lst = txt.split(' ')
            features.append((lst, dir_name))
            f.close()
    return features