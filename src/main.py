#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/22 11:39
@Description:

"""
__author__ = 'Lich'

from src.bayes import *

def main():
    post_list, class_vec = load_data_set()
    ls = create_vocab_list(post_list)
    print ls, len(ls)
    matrix = []
    for post_doc in post_list:
        temp = create_word_to_vec(ls, post_doc)
        print temp, len(temp)
        matrix.append(temp)
    p0, p1, p_bad = train_native_bayes(matrix, class_vec)
    print p0,p1
    test = ['dog', 'good', 'nice']
    doc_vec = create_word_to_vec(ls, test)
    res = classify_native_bayes(doc_vec, p0, p1, p_bad)
    print res


if __name__ == '__main__':
    # main()
    list = [1,2,3,4,5,6,7,8,9]
    print list[::2]
    print list[1::2]

