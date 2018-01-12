#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:lch02
@Time:  2017/12/15 14:40
@Description: 
"""
import os

__author__ = 'lch02'

# 模型存储位置
model_path = os.path.join(os.path.abspath('..'), 'model')
feature_path = os.path.join(os.path.abspath('..'), 'features')
material_path =  os.path.join(os.path.abspath('..'), 'material')
test_path =  os.path.join(os.path.abspath('..'), 'test')
verify_path = os.path.join(os.path.abspath('..'), 'verify')

# tf-idf阈值
threshold = 0.02

dirs = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology', 'social_fr', 'political_fr', 'international_fr', 'economy_fr']
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology', 'social_fr', 'political_fr', 'international_fr', 'economy_fr']
fr_categories = ['social_fr', 'political_fr', 'international_fr', 'economy_fr']

verifies = ['culture', 'economy', 'energy', 'environment', 'political', 'technology']

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
