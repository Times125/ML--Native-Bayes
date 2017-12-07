#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/12/4 10:53
@Description: 
"""
import nltk

__author__ = 'Lich'

'''
朴素贝叶斯分类器
'''
categories = ['culture', 'economy', 'energy', 'environment', 'political', 'security', 'technology']
train_set = []
test_set = []


def native_bayes_classifier(features, post_list, vocab_set=None):
    global word_features
    word_features = features

    train_set = post_list[::2]
    test_set = post_list[1::2]

    train_data = [(doc_features(doc, category), category) for (doc, category) in train_set]
    test_data = [(doc_features(doc, category), category) for (doc, category) in test_set]

    # print train_set, '\n\n'
    # print test_set, '\n\n'
    # print train_data, '\n\n'
    print test_data[5]
    # print len(train_set), len(test_set)

    cul = {u'contains(monoxide)': False, u'contains(alec)': False, u'contains(ambitious)': False,
           u'contains(writes)': True, u'contains(fate)': False, u'contains(voorhees)': False,
           u'contains(blazing)': False, u'contains(warmth)': False, u'contains(d-day)': False,
           u'contains(handful)': False, u'contains(boo)': False, u'contains(obstacle)': False,
           u'contains(teenager)': False, u'contains(minority)': False, u'contains(protect)': True,
           u'contains(key)': False, u'contains(led)': True, u'contains(explained)': False, u'contains(nasty)': False,
           u'contains(sporting)': False, u'contains(dwells)': False, u'contains(jones)': False,
           u'contains(pack)': False, u'contains(claim)': False, u'contains(tuition)': False, u'contains(clean)': False,
           u'contains(underline)': False, u'contains(bringing)': True, u'contains(wise)': False,
           u'contains(vietnam)': False, u'contains(broadening)': False, u'contains(resentment)': False,
           u'contains(fed)': False, u'contains(confidant)': False, u'contains(andy)': False,
           u'contains(doisneau)': False, u'contains(wild)': True, u'contains(eco-warrior)': False,
           u'contains(democrat)': False, u'contains(wilson)': False, u'contains(surface)': False,
           u'contains(pity)': False, u'contains(ranked)': False, u'contains(mount)': False, u'contains(slang)': False,
           u'contains(taking)': True, u'contains(giles)': False, u'contains(columnist)': False,
           u'contains(russell)': False, u'contains(warrant)': False, u'contains(mellowed)': False,
           u'contains(mounting)': False, u'contains(certain)': False, u'contains(arriving)': False,
           u'contains(shelf)': False, u'contains(stage-play)': False, u'contains(grave)': False,
           u'contains(die)': False, u'contains(magnificent)': False, u'contains(possessive)': False,
           u'contains(savaging)': False, u'contains(share)': False, u'contains(settlement)': False,
           u'contains(fossil)': False, u'contains(meet)': False, u'contains(dent)': False,
           u'contains(gallantry)': False, u'contains(statement)': False, u'contains(bass)': False,
           u'contains(wardrobe)': False, u'contains(bloomsbury)': True, u'contains(marriage)': True,
           u'contains(ewht)': False, u'contains(sisterhood)': False, u'contains(flower)': False,
           u'contains(time-straddling)': False, u'contains(dog)': False, u'contains(subscriber)': False,
           u'contains(leave)': False, u'contains(stripe)': False, u'contains(medium)': False, u'contains(good)': False,
           u'contains(live)': False, u'contains(unlikely)': False, u'contains(b-movie)': False,
           u'contains(billboard)': False, u'contains(hawk)': False, u'contains(lump)': False,
           u'contains(heartbreak)': False, u'contains(battler)': False, u'contains(bauman)': False,
           u'contains(smile)': False, u'contains(mandolin)': False, u'contains(spanish-speaking)': False}
    classifier = nltk.classify.NaiveBayesClassifier.train(train_data)
    for i in range(0, len(test_data)):
        print '分类结果', classifier.classify(test_data[i][0])
    print classifier.classify(cul)
    print 'test_accuracy is %.4f' % nltk.classify.accuracy(classifier, test_data)


'''
构建一个字典，主要表示输入文档的单词，是否出现在自己构建的语料库中
'''


def doc_features(doc, category):
    doc_words = set(doc)
    features = {}
    if category == categories[0]:
        for word in word_features[0][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[1]:
        for word in word_features[1][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[2]:
        for word in word_features[2][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[3]:
        for word in word_features[1][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[4]:
        for word in word_features[2][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[5]:
        for word in word_features[1][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == categories[6]:
        for word in word_features[2][0]:
            features['contains(%s)' % word] = (word in doc_words)
    return features
