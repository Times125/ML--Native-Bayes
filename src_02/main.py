#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 
"""
__author__ = 'Lich'

from  nltk_bayes_classifier import *

def main():
    for i in range(1, 26):
        text_parse(open(u'G:\\机器学习源码\\MLiA_SourceCode\\machinelearninginaction\\Ch04\\email\\ham\\%d.txt' %i).read())
    pass


if __name__ == '__main__':
    main()