#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lch02
@Time:  2017/12/15 14:40
@Description: 
"""
__author__ = 'lch02'

# 模型存储位置
model_path = r'E:\Repositories\ML--Native-Bayes\model'

feature_path = r'E:\Repositories\ML--Native-Bayes\features'
# eng_f_path = r'/Users/lch/Desktop/pycharm/Bayes/features'
material_path = r'E:\Repositories\ML--Native-Bayes\material'
# eng_m_path = r'/Users/lch/Desktop/pycharm/Bayes/material'
test_path = r'E:\Repositories\ML--Native-Bayes\test'
# eng_test_path = r'/Users/lch/Desktop/pycharm/Bayes/test'

# tf-idf阈值
threshold = 0.02

dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology', 'social_fr', 'political_fr', 'international_fr', 'economy_fr']
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology', 'social_fr', 'political_fr', 'international_fr', 'economy_fr']

'''
# 法语
fre_dirs = ['economy', 'international', 'political', 'social']
fre_categories = ['economy', 'international', 'political', 'social']
# french
fre_f_path = r'E:\Repositories\ML--Native-Bayes\features_fre'
# fre_f_path = r'/Users/lch/Desktop/pycharm/Bayes/features'
fre_m_path = r'E:\Repositories\ML--Native-Bayes\material_fre'
# fre_m_path = r'/Users/lch/Desktop/pycharm/Bayes/material'
fre_test_path = r'E:\Repositories\ML--Native-Bayes\test_fre'
# fre_test_path = r'/Users/lch/Desktop/pycharm/Bayes/test'
'''
