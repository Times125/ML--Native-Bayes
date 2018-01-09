#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/4 10:53
@Description: 
"""
import nltk
import random
from import_data import *
from sklearn.svm import LinearSVC
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
    testss(classifier)  # 0.86826
    print 'NB test_accuracy is %.7f' % nltk.classify.accuracy(classifier, test_data) # 1.00

    svm_classifier = nltk.SklearnClassifier(LinearSVC()).train(train_data)
    testss(svm_classifier)  # 0.85858
    print 'SVM test_accuracy is %.7f' % nltk.classify.accuracy(svm_classifier, test_data) # 0.9869338

    # dTree_classifier = nltk.classify.DecisionTreeClassifier.train(train_data)
    # testss(dTree_classifier) # 0.00798
    # print 'DecisionTree test_accuracy is %.7f' % nltk.classify.accuracy(dTree_classifier, test_data)   #0.9939024

    # maxent_classifier = nltk.classify.MaxentClassifier.train(train_data)
    # testss(maxent_classifier) # 0.37325
    # print 'MaxentClassifier test_accuracy is %.7f' % nltk.classify.accuracy(maxent_classifier, test_data) # 0.0836237

    with open(os.path.join(model_path, 'nb_classifier.pkl'), 'wb') as f:
        pickle.dump(classifier, f)

def testss(classifier):
    with open(os.path.join(model_path, 'all_words.pkl'), 'rb') as f:
        all_words = pickle.load(f)
    total_num = 0
    uncorrected = 0
    for dir_name in verifies:
        file_path = os.path.join(verify_path, dir_name)
        file_num = len(os.listdir(file_path))
        total_num += file_num
        b = 0
        for i in range(file_num):
            fn = os.path.join(file_path, str(b) + r'.txt')
            with codecs.open(fn, 'rb', 'utf-8') as reader:
                txt = reader.read().decode('utf-8')
            res = classify_text(txt, classifier, all_words)
            if res != dir_name:
                uncorrected += 1
                print dir_name, ":", b, '.txt'
            b += 1
    print total_num, '  ', uncorrected
    print 'accuracy is : %.5f' % (1 - (uncorrected / float(total_num)))

def classify_text(txt, classifier, all_words):
    from text_processing import text_parse
    res_word_list, v = text_parse(txt)
    wait_for_class = {}
    for item in res_word_list:
        wait_for_class['contains(%s)' % item] = (item in all_words)
    res = classifier.classify(wait_for_class)
    return res


'''
获取保存的模型
'''
def get_model():
    with open(os.path.join(model_path, 'nb_classifier.pkl'), 'rb') as f:
        nb_classifier = pickle.load(f)
    return nb_classifier


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
