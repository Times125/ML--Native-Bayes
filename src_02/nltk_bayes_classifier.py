#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/4 10:53
@Description: 
"""
import nltk
import pickle
from import_data import *
__author__ = 'Lich'

'''
朴素贝叶斯分类器
'''
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
train_set = []
test_set = []


def train_native_bayes_classifier(m_features, post_list, vocab_set=None):

    global word_features
    word_features = m_features   # [(lst1,cat1),(lst2,cat2),...,(lst7,cat7)]

    train_set = post_list[::2]  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
    test_set = post_list[1::2]

    train_data = [(doc_features(doc, category), category) for (doc, category) in train_set]
    test_data = [(doc_features(doc, category), category) for (doc, category) in test_set]

    classifier = nltk.classify.NaiveBayesClassifier.train(train_data)
    f = open(os.path.join(mac_f_path, 'my_classifier_pickle'), 'wb')
    pickle.dump(classifier, f)
    f.close()

    # for i in range(0, len(test_data)):
    #   print u'分类结果', classifier.classify(test_data[i][0])
    print 'test_accuracy is %.4f' % nltk.classify.accuracy(classifier, test_data)

'''
获取保存的模型
'''
def get_model():
    f = open(os.path.join(mac_f_path, 'my_classifier_pickle'), 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


'''
构建一个字典，主要表示输入文档的单词，是否出现在自己构建的语料库中
'''


def doc_features(doc, category):
    print type(doc)
    doc_words = set(doc)
    d_features = {}
    if category == categories[0]:
        for word in word_features[0][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[1]:
        for word in word_features[1][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[2]:
        for word in word_features[2][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[3]:
        for word in word_features[3][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[4]:
        for word in word_features[4][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[5]:
        for word in word_features[5][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[6]:
        for word in word_features[6][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    return d_features
