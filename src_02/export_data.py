#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/6 13:27
@Description: 计算出的将特征值保存到文件
"""
__author__ = 'Lich'
import codecs
import time
import os
from text_processing import get_class_features
from file_path_constant import *

__author__ = 'Lich'

categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']

'''
建立特征库
'''
def build_features_lib():
    print u'正在导出特征，请等待...'
    start_time = time.time()
    l_features = get_class_features()  # 这是自己建立的语料库 [(lst1,cat1),(lst2,cat2),...,(lst7,cat7)]
    for item in l_features:
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
    print u'特征库导出完成！ 一共耗时%.4f秒' % (end_time - start_time)
    return 0

def write_to_file(item):
    if not os.path.exists(mac_f_path):
        print 'nonononononononononon!!!'
        os.makedirs(mac_f_path)
    else:
        try:
            f = codecs.open(os.path.join(mac_f_path, item[1]) + r'.txt', 'wb', 'utf-8')
            txt = ' '.join(item[0])  # list 转 str
            f.write(txt)
        except IOError, e:
            print item[1], u'特征库导出异常，IOError ', e.message
        finally:
            f.close()
