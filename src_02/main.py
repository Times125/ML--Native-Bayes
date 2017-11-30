#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本总数为20，其中垃圾邮件10份，普通邮件10份。训练样本占总文本集合的1/2
"""
__author__ = 'Lich'

from nltk_bayes_classifier import *


def main():
    post_list = []
    for i in range(1, 21):
        post_list.append(text_parse(open(u'C:\\Users\\Lich\\Desktop\\email\\%d.txt' % i).read()))
    get_features(post_list)
    # print post_list


if __name__ == '__main__':
    main()
