#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/6 13:27
@Description: 计算出的将特征值保存到文件
"""
import codecs
import time
import os
from text_processing import get_class_features

__author__ = 'Lich'
win_f_path = r'G:\Repositories\ML--Native-Bayes\features'
mac_f_path = r'/Users/lch/Desktop/pycharm/Bayes/features'
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']


def build_features_lib():
    print '正在导出特征，请等待...'
    start_time = time.time()
    features = get_class_features()  # 这是自己建立的语料库
    for item in features:
        if item[1] == categories[0]:
            write_to_file(item)
        elif item[1] == categories[1]:
            write_to_file(item)
        elif item[1] == categories[2]:
            write_to_file(item)
        elif item[1] == categories[3]:
            write_to_file(item)
        elif item[1] == categories[4]:
            write_to_file(item)
        elif item[1] == categories[5]:
            write_to_file(item)
        elif item[1] == categories[6]:
            write_to_file(item)
    end_time = time.time()
    print '特征库导出完成！ 一共耗时%.4f秒' % (end_time - start_time)

def write_to_file(item):
    if not os.path.exists(win_f_path):
        os.makedirs(win_f_path)
    else:
        f = codecs.open(win_f_path + u'\\' + item[1] + r'.txt', 'w', 'utf-8')
        f.write(' '.join(item[0]))
        f.close()
