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
categories = ['env', 'eco', 'pol']
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
    # print test_data
    # print len(train_set), len(test_set)
    env_tmp = {u'contains(abundance)': False, u'contains(climate)': True, u'contains(michelle)': False,
               u'contains(trump-owned)': False, u'contains(weight)': False, u'contains(mass)': False,
               u'contains(atmospheric)': False, u'contains(strongest)': False, u'contains(rock)': False,
               u'contains(enabled)': False, u'contains(concept)': False, u'contains(platoon)': False,
               u'contains(risk)': False, u'contains(chile)': False, u'contains(population)': False,
               u'contains(moment)': False, u'contains(consultation)': False, u'contains(marcelo)': False,
               u'contains(declared)': False, u'contains(occurs)': False, u'contains(exalted)': False,
               u'contains(tropical)': True, u'contains(creation)': False, u'contains(flooding)': False,
               u'contains(strength)': True, u'contains(storm)': True}
    pol_tmp = {u'contains(suing)': False, u'contains(insurance)': False, u"contains(city's)": False,
               u'contains(subsidy)': False, u'contains(janelle)': False, u'contains(cradle)': False,
               u'contains(washington)': False, u'contains(white)': True, u'contains(politics)': False,
               u'contains(mr)': True, u"contains(baltimore's)": False, u'contains(wall)': False,
               u'contains(trade)': False, u'contains(fact-check)': False, u'contains(capitol)': False,
               u'contains(warned)': False, u'contains(tower)': False, u'contains(cancellation)': False,
               u'contains(kuttner)': False, u'contains(marched)': False, u'contains(fringe)': False,
               u'contains(hate)': False, u'contains(growing)': False, u'contains(trump)': True}
    pol_tmp2 = {u'contains(percent)': False, u'contains(cost-sharing)': False, u'contains(center)': False,
                u'contains(mayor)': False, u'contains(paula)': False, u'contains(ellen)': False,
                u'contains(rally)': True, u'contains(lindsey)': False, u'contains(alt-left)': False,
                u'contains(prospect)': False, u'contains(encourage)': False, u'contains(covering)': False,
                u'contains(renaming)': False, u'contains(lee)': False, u'contains(county)': False,
                u'contains(payment)': False, u'contains(attorney)': False, u'contains(treason)': False,
                u'contains(attack)': False, u'contains(help)': False, u'contains(obamacare)': False,
                u'contains(alabama)': False, u'contains(neo-nazis)': False, u'contains(blackened)': False,
                u'contains(e)': False, u"contains(he's)": False, u'contains(military)': False,
                u'contains(william)': False, u'contains(equivalency)': False, u'contains(guilt)': False,
                u'contains(strategist)': False, u'contains(flag)': False, u'contains(gotta)': False,
                u'contains(seeing)': False, u'contains(press)': False, u'contains(child)': False,
                u"contains(it's)": False, u'contains(diehl)': False, u'contains(courthouse)': False,
                u'contains(legislation)': False, u'contains(identity)': False, u'contains(re-ignited)': False,
                u'contains(statue)': False, u'contains(jefferson)': False}

    classifier = nltk.classify.NaiveBayesClassifier.train(test_data)
    for i in range(0,len(test_data)):
        print '分类结果', classifier.classify(test_data[i][0])
    print 'env_tmp is ', classifier.classify(env_tmp)
    print 'pol_tmp is', classifier.classify(pol_tmp)
    print 'pol_tmp2 is', classifier.classify(pol_tmp2)
    print 'test_accuracy is %d' % nltk.classify.accuracy(classifier, train_data)


'''
获得
'''


def doc_features(doc, category):
    doc_words = set(doc)
    features = {}
    if category == 'env':
        for word in word_features[0][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == 'eco':
        for word in word_features[1][0]:
            features['contains(%s)' % word] = (word in doc_words)
    elif category == 'pol':
        for word in word_features[2][0]:
            features['contains(%s)' % word] = (word in doc_words)
    return features
