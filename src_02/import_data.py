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

reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'Lich'


def import_data_from_csv():
    print '正在导入，请等待...'
    start_time = time.time()
    log_info = {}
    dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
    for dir_name in dirs:
        csv_reader = csv.reader(
            codecs.open(r'C:\Users\Lich\Desktop\material' + u'\\' + dir_name + u'\\' + dir_name + r'.csv', 'r', 'gbk'))
        a = 1
        for row in csv_reader:
            if len(row) == 0:
                pass
            else:
                f = codecs.open(r'C:\Users\Lich\Desktop\material' + u'\\' + dir_name + u'\\' + str(a) + r'.txt', 'w','utf-8')
                txt = str(row[0]).decode('gbk').encode('utf-8')
                f.write(txt)
                f.close()
                a += 1
        log_info[dir_name] = a
    end_time = time.time()
    for item in log_info:
        print item, '类新闻共%d篇' % log_info[item]
    print 'CSV文件导入TXT完成！ 一共耗时%.4f秒' % (end_time - start_time)


def import_data_from_csv2():
    print '正在导入，请等待...'
    start_time = time.time()
    log_info = {}
    dirs = ['eco', 'env', 'pol']
    for dir_name in dirs:
        csv_reader = csv.reader(
            open(r'G:\Repositories\ML--Native-Bayes\material' + u'\\' + dir_name + u'\\' + dir_name + r'.csv', 'r'))
        a = 1
        for row in csv_reader:
            if len(row) == 0:
                pass
            else:
                f = codecs.open(r'G:\Repositories\ML--Native-Bayes\material' + u'\\' + dir_name + u'\\' + str(a) + r'.txt', 'w', 'utf-8')
                txt = str(row[0]).decode('gbk').encode('utf-8')
                f.write(txt)
                f.close()
                a += 1
        log_info[dir_name] = a
    end_time = time.time()
    for item in log_info:
        print item, '类新闻共%d篇' % log_info[item]
    print 'CSV文件导入TXT完成！ 一共耗时%.4f秒' % (end_time - start_time)
