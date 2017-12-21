#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/4 10:53
@Description: 
"""
import nltk
import pickle
import random
from import_data import *
__author__ = 'Lich'

'''
朴素贝叶斯分类器
'''
train_set = []
test_set = []

def train_native_bayes_classifier(m_features, post_list, vocab_set=None):
    global word_features
    word_features = m_features   # [(lst1,cat1),(lst2,cat2),...,(lst7,cat7)]
    random.shuffle(post_list)  # 打乱顺序
    lst_sum = len(post_list)
    pre = int(round(lst_sum * 0.8))  # 前80%的数据作为训练集,后20%的数据作为测试集
    train_set = post_list[:pre]  # [('文档所含单词集','类别'),..,('文档所含单词集','类别')]
    test_set = post_list[pre:]

    train_data = [(doc_features(doc, category), category) for (doc, category) in train_set]
    test_data = [(doc_features(doc, category), category) for (doc, category) in test_set]
    classifier = nltk.classify.NaiveBayesClassifier.train(train_data)
    print 'test_accuracy is %.7f' % nltk.classify.accuracy(classifier, test_data)

    # 交叉验证
    aft = int(round(lst_sum * 0.2))
    j_train_set = post_list[aft:]  # [('文档所含单词集','类别'),..,('文档所含单词集','类别')]
    j_test_set = post_list[:aft]

    j_train_data = [(doc_features(doc, category), category) for (doc, category) in j_train_set]
    j_test_data = [(doc_features(doc, category), category) for (doc, category) in j_test_set]
    classifier = nltk.classify.NaiveBayesClassifier.train(j_train_data)
    print 'j_test_accuracy is %.7f' % nltk.classify.accuracy(classifier, j_test_data)

    """
    print len(train_data), '--', len(test_data)
    print len(train_set), '--', len(test_set)
    for it in test_data:
        res = classifier.classify(it[0])
        if not (it[1] == res):
            print it[1]
    """

    f = open(os.path.join(model_path, 'my_classifier_pickle'), 'wb')
    pickle.dump(classifier, f)
    f.close()

'''
获取保存的模型
'''
def get_model():
    f = open(os.path.join(model_path, 'my_classifier_pickle'), 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


'''
构建一个字典，主要表示输入文档的单词，是否出现在自己构建的语料库中
'''
def doc_features(doc, category):
    doc_words = set(doc)
    d_features = {}
    for wf in word_features:
        if category == wf[1]:
            cat_words = set(wf[0])
            for word in cat_words:
                d_features['contains(%s)' % word] = (word in doc_words)
    """
    if category == categories[0]:
        print category, '----', category == word_features[0][1]
        for word in word_features[0][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[1]:
        print category, '----', category == word_features[1][1]
        for word in word_features[1][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[2]:
        print category, '----', category == word_features[2][1]
        for word in word_features[2][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[3]:
        print category, '----', category == word_features[3][1]
        for word in word_features[3][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[4]:
        print category, '----', category == word_features[4][1]
        for word in word_features[4][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[5]:
        print category, '----', category == word_features[5][1]
        for word in word_features[5][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[6]:
        print category, '----', category == word_features[6][1]
        for word in word_features[6][0]:
            d_features['contains(%s)' % word] = (word in doc_words)
    """
    return d_features
