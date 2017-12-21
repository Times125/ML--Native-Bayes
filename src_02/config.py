#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lch02
@Time:  2017/12/15 14:40
@Description: 
"""
__author__ = 'lch02'

mac_f_path = r'E:\Repositories\ML--Native-Bayes\features'
# mac_f_path = r'/Users/lch/Desktop/pycharm/Bayes/features'
mac_path = r'E:\Repositories\ML--Native-Bayes\material'
# mac_path = r'/Users/lch/Desktop/pycharm/Bayes/material'
mac_test_path = r'E:\Repositories\ML--Native-Bayes\test'
# mac_test_path = r'/Users/lch/Desktop/pycharm/Bayes/test'

# eng
dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']

# tf-idf阈值
threshold = 0.02