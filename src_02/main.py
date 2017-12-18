#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:Lich
@Time:  2017/11/29 10:35
@Description: 训练样本包括：环境类、政治类、经济类、文化类、技术类、安全类和能源类文本
"""
import getopt
import time
import sys
import os
import codecs
from file_path_constant import *
from nltk_bayes_classifier import import_features_from_lib, get_model
from nltk_bayes_classifier import import_data_from_excel, train_native_bayes_classifier
from export_data import build_features_lib
from text_processing import text_parse
from multiprocessing import Pool, Manager,Queue


__author__ = 'Lich'


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'heltc:', ['classify=', 'help', 'excel', 'train', 'lib'])
    except getopt.GetoptError:
        sys.exit(-1)
    for opt, value in opts:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-e', '--excel'):
            import_data_from_excel()
        if opt in ('-l', '--lib'):
            build_features_lib()
        if opt in ('-t', '--train'):
            train()
        if opt in ('-c', '--classify'):
            res = classify_text(' '.join(args))
            print u'分类结果', res
            sys.exit(res)


def classify_text(txt):
    classifier = get_model()
    features, all_words = import_features_from_lib()
    res_word_list, v = text_parse(txt)
    wait_for_class = {}
    for item in res_word_list:
        wait_for_class['contains(%s)' % item] = (item in all_words)
    res = classifier.classify(wait_for_class)
    print res
    return res

def usage():
    print (u'所有命令参数 -e: 从Excel 里导入数据 -l: 建立特征库 -t: 训练模型 -c: 输入一篇文章进行分类\n')
    print(u'如何使用？请看示例:\n')
    print(u'1) 查看帮助：[python main.py -h] 或者 [python main.py --help]\n')
    print(u'2) 从Excel 里导入数据:[python main.py -e]\n')
    print(u'3) 建立特征库:[python main.py -l]\n')
    print(u'4) 训练模型:[python main.py -t]\n')
    print(u'5) 输入一篇文章进行分类:[python main.py -c: \"hello word!\"] 或者 [python main.py --classify= \"hello word!\"]\n')

def train():
    start_time = time.time()
    features, all_words = import_features_from_lib()  # 这是自己建立的语料库
    mid_time2 = time.time()
    vocab_set = set([])
    post_list = []

    man = Manager()
    queue_pool = man.Queue()
    pool_t = Pool(7)  # 开7个进程
    print 'Parent process ID %d' % os.getpid()
    for dir_name in dirs:
        pool_t.apply_async(deal_train_doc, (dir_name, queue_pool,))
    pool_t.close()
    pool_t.join()

    print queue_pool.empty()
    while not queue_pool.empty():
        res = queue_pool.get(True)  # (p_post_list, dir_name, p_vocab_set)
        for lst in res[0]:
            print lst
            post_list.append((lst, res[1]))
        vocab_set = vocab_set | res[2]
    
    '''
    # 程序耗时部分1，需要修改
    for dir_name in dirs:
        files_num = len(os.listdir(os.path.join(mac_path, dir_name)))  # 一个类目录下文件数量
        print files_num
        fp = os.path.join(mac_path, dir_name)
        for i in range(files_num/2, files_num):
            f = codecs.open(os.path.join(fp, r'%d.txt' % i), 'r', 'utf-8')
            txt = f.read()
            res_word_list, doc_set = text_parse(txt)  # 读取测试文本
            post_list.append((res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
            vocab_set = vocab_set | doc_set
            f.close()
    '''
    mid_time = time.time()
    print 'read test files cost total time %.4f seconds' % (mid_time - mid_time2)  # 847秒 / 419s
    
    train_native_bayes_classifier(features, post_list, vocab_set)

    end_time = time.time()
    print 'method train() cost total time %.4f seconds' % (end_time - start_time)  #

def deal_train_doc(dir_name, queue_pool):
    import os
    p_post_list = []
    p_vocab_set = set([])
    fp = os.path.join(mac_path, dir_name)
    files_num = len(os.listdir(fp))  # 一个类目录下文件数量
    print u'此目录下共%d个txt文件' % files_num, 'deal_train_doc subprocess id %d' % os.getpid()
    for i in range(files_num / 2, files_num):
        f = codecs.open(os.path.join(fp, r'%d.txt' % i), 'rb', 'utf-8')
        txt = f.read()
        p_res_word_list, p_doc_set = text_parse(txt)  # 读取测试文本
        p_post_list.append((p_res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
        p_vocab_set = p_vocab_set | p_doc_set
        f.close()
    print len(p_post_list), dir_name
    queue_pool.put((p_post_list, dir_name, p_vocab_set))

def tests():
    train = [({'a': 1, 'b': 0, 'c': 1}, 'y'),
             ({'a': 1, 'b': 0, 'c': 0}, 'y'),
             ({'a': 1, 'b': 1, 'c': 1}, 'x'),
             ({'a': 1, 'b': 1, 'c': 0}, 'x'),
             ({'a': 1, 'b': 1, 'c': 1}, 'x'),
             ({'a': 0, 'b': 0, 'c': 1}, 'y')]
    test = [({'a': 1, 'b': 0, 'c': 1}, 'y'),
            ({'a': 0, 'b': 0, 'c': 1}, 'y'),
            ({'a': 1, 'b': 0, 'c': 0}, 'y'),
            ({'a': 1, 'b': 1, 'c': 0}, 'x'),
            ({'a': 1, 'b': 1, 'c': 1}, 'x')]
    testp = [({'a': 1, 'b': 0, 'c': 1}),
             ({'a': 0, 'b': 0, 'c': 1}),
             ({'a': 1, 'b': 0, 'c': 0}),
             ({'a': 1, 'b': 1, 'c': 0}),
             ({'a': 1, 'b': 1, 'c': 1})]
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
    cla = get_model()
    print cla.classify(cul)


if __name__ == '__main__':
    # main()  # 运行程序
    # import_data_from_excel()
    # build_features_lib()
    train()
    # classify_text()
