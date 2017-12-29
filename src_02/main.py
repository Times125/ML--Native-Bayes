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
import re
import socket
import pickle
from openpyxl import load_workbook
from config import *
from nltk_bayes_classifier import import_features_from_lib, get_model
from nltk_bayes_classifier import import_data_from_excel, train_native_bayes_classifier
from export_data import build_features_lib
from text_processing import text_parse
from multiprocessing import Pool, Manager,Queue

__author__ = 'Lich'


def main():
    classifier = get_model()
    with open(os.path.join(model_path, 'all_words.pkl'), 'rb') as f:
        all_words = pickle.load(f)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9898))
    s.listen(10)
    while True:
        sock, addr = s.accept()
        data = sock.recv(102400)
        data = data.decode('utf-8').encode('utf-8')
        if data is 'auto':
            import_data_from_excel()
            build_features_lib()
            import_features_from_lib()  # 这是自己建立的语料库
            train()
            sock.send("complete auto!")
            continue
        res = classify_text(data, classifier, all_words)
        sock.send(res)


def classify_text(txt, classifier, all_words):
    res_word_list, v = text_parse(txt)
    wait_for_class = {}
    for item in res_word_list:
        wait_for_class['contains(%s)' % item] = (item in all_words)
    res = classifier.classify(wait_for_class)
    return res


def train():
    start_time = time.time()
    with open(os.path.join(model_path, 'features.pkl'), 'rb') as f:
        features = pickle.load(f)
    mid_time2 = time.time()
    vocab_set = set([])
    post_list = []

    man = Manager()
    queue_pool = man.Queue()
    pool_t = Pool(len(dirs))  # 开n个进程

    print 'Parent process ID %d' % os.getpid()
    for dir_name in dirs:
        pool_t.apply_async(deal_train_doc, (dir_name, queue_pool,))
    pool_t.close()
    pool_t.join()

    print queue_pool.empty()
    while not queue_pool.empty():
        res = queue_pool.get(True)  # (p_post_list, p_vocab_set)
        for lst in res[0]:
            post_list.append(lst)
        vocab_set = vocab_set | res[1]

    mid_time = time.time()
    print 'read test files cost total time %.4f seconds' % (mid_time - mid_time2)  # 847秒 / 419s
    train_native_bayes_classifier(features, post_list, vocab_set)
    end_time = time.time()
    print 'method train() cost total time %.4f seconds' % (end_time - start_time)  #

def deal_train_doc(dir_name, queue_pool):
    import os
    p_post_list = []
    p_vocab_set = set([])
    fp = os.path.join(material_path, dir_name)
    files_num = len(os.listdir(fp))  # 一个类目录下文件数量
    print dir_name, u'此目录下共%d个txt文件' % files_num, 'deal_train_doc subprocess id %d' % os.getpid()
    for i in range(files_num / 2, files_num):
        with codecs.open(os.path.join(fp, r'%d.txt' % i), 'rb', 'utf-8') as reader:
            txt = reader.read()  # .decode('utf-8')
            p_res_word_list, p_doc_set = text_parse(txt)  # 读取测试文本
            p_post_list.append((p_res_word_list, dir_name))  # [('文档所含单词集','类别'),('文档所含单词集','类别')]
            p_vocab_set = p_vocab_set | p_doc_set
    print len(p_post_list), dir_name
    queue_pool.put((p_post_list, p_vocab_set))

'''
创建程序必要的文件目录
'''

def check_dirs():
    f_path = os.path.join(feature_path)
    t_path = os.path.join(test_path)
    mod_path = os.path.join(model_path)

    for dir_name in verifies:
        v_path = os.path.join(verify_path, dir_name)
        if not os.path.exists(v_path):
            os.makedirs(v_path)

    if not os.path.exists(mod_path):
        os.makedirs(mod_path)

    for dir_name in dirs:
        m_path = os.path.join(material_path, dir_name)
        if not os.path.exists(m_path):
            os.makedirs(m_path)
        if not os.path.exists(f_path):
            os.makedirs(f_path)
        if not os.path.exists(t_path):
            os.makedirs(t_path)

def tests():
    classifier = get_model()
    with open(os.path.join(model_path, 'all_words.pkl'), 'rb') as f:
        all_words = pickle.load(f)
    for dir_name in verifies:
        wb = load_workbook(os.path.join(verify_path, dir_name + r'.xlsx'))
        sheet = wb.get_sheet_by_name("sheet1")
        tmp_path = os.path.join(verify_path, dir_name)
        a = 0
        for row in sheet['A']:
            file_name = os.path.join(tmp_path, str(a) + r'.txt')
            txt = str(row.value).decode('ISO-8859-15').encode('utf-8')
            if dir_name not in fr_categories:
                txt = re.sub(r'[^\x00-\x7F]+', '', txt)  # 去除所有非英语字符
            else:
                txt = re.sub(r'[^\x00-\xFF]+', '', txt)  # 去除所有非法语字符
            if not txt or len(txt) <= 150:  # 舍弃过短的文章
                continue
            with codecs.open(file_name, 'wb', 'utf-8', errors='ignore') as writer:
                writer.write(txt)
                a += 1
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
            print res, '<----------------> ', dir_name
            if res != dir_name:
                uncorrected += 1
                print dir_name, ":", b, '.txt'
            b += 1
    print total_num, '  ', uncorrected
    print 'nb_classifier accuracy is : %.5f' % (1 - (uncorrected / float(total_num)))


if __name__ == '__main__':
    check_dirs()
    main()  # 运行程序
    # import_data_from_excel()
    # build_features_lib()
    # import_features_from_lib()
    # train()
    # tests()
    # inter
    #classify_text(u'Le chasseur de 1ere claisse Albéric Riveta est décédé dans la nuit du 17 au 18 juin près de Gao, au Mali Le soldat français faisait partie du 1er régiment de chasseurs parachutistes de Pamiers (Ariège).  L\'Elysée a annoncé, dimanche soir, dans un communiqué, «la mort accidentelle», la nuit précédente, d\'un soldat français, Albéric Riveta, «lors d\'une opération aéroportée» au Mali. La présidence s\'est refusée à donner toute précision sur les circonstances de ce décès.    «Le président de la République a appris avec tristesse la mort accidentelle la nuit dernière au Mali d\'un soldat du 1er régiment de chasseurs parachutistes de Pamiers (Ariège) lors d\'une opération aéroportée effectuée dans la région d\'Almoustarat», au nord de Gao, a déclaré la présidence. Au cours de cette opération, d\'autres soldats ont été blessés.    Dans un communiqué, la ministre des Armées, Sylvie Goulard, déclare avoir appris «avec tristesse et émotion la mort accidentelle en opération au Mali, dans la nuit du 17 au 18 juin 2017, du chasseur parachutiste de 1ère classe Albéric Riveta». Elle «rend hommage à ce parachutiste tombé pour la France dans l’accomplissement de sa mission et assure sa famille et ses frères d’armes de son plein soutien dans cette douloureuse épreuve», poursuit le communiqué.      Emmanuel Macron a «exprimé sa confiance et sa fierté aux militaires français qui combattent avec courage les groupes armés terroristes au Sahel» et «réitéré le soutien de la France au Mali et à la force des Nations Unies pour la mise en oeuvre de l\'accord de paix», a déclaré l\'Elysée dans son communiqué. Environ 4 000 hommes sont déployés au Mali et dans d\'autres pays d\'Afrique dans le cadre de l\'opération Barkhane.     Le chef de l\'Etat a également salué «la mémoire de ce militaire français tué dans l\'accomplissement de sa mission pour la défense de notre pays et la protection de nos concitoyens» et adressé «ses sincères condoléances à sa famille, ses amis et ses frères d\'armes», toujours selon la présidence.   Cinq soldats maliens ont encore été tués samedi et huit blessés dans l\'attaque d\'un camp militaire dans le nord du Mali. Ce décès porte à 18 le nombre de soldats français tué depuis le début des opérations au Mali en janvier 2013.')
    # tec
    #classify_text(u'Google plans to stop Amazon\'s Fire TV streaming devices being able to use YouTube from the start of 2018. The search giant has also blocked a workaround that Amazon introduced to restore YouTube access to a screen-based version of its smart speaker. Experts say the steps mark an escalation of a business row in which consumers have been caught up in the fallout. Amazon had previously stopped selling several of Google\'s hardware products. It removed the latest Nest-branded smart home kit - including a home security system and a new version of its thermostat - from its online stores last month. And since 2015, Amazon has refused to sell Google\'s Chromecast video and audio-streaming dongles. The latest development coincides with the release of Amazon\'s Prime Video app for the Apple TV. Its absence had previously put Apple\'s set-top box at a disadvantage to Amazon\'s Fire TV line-up. Fire TV owners have reported that trying to watch YouTube clips now prompts an alert warning them that they will lose the functionality on 1 January. I use firestick to watch YouTube primarily and suddenly this message appears today. No #youtube on #FireTV from 1/1/18. Great! pic.twitter.com/Pe53chi4ft End of Twitter post by @eqbalashraf "We\'ve been trying to reach agreement with Amazon to give consumers access to each other\'s products and services," Google said in a statement. "But Amazon doesn\'t carry Google products like Chromecast and Google Home, doesn\'t make Prime Video available for Google Cast users, and last month stopped selling some of Nest\'s latest products. "Given this lack of reciprocity, we are no longer supporting YouTube on Echo Show and FireTV. We hope we can reach an agreement to resolve these issues soon." Google had stopped Amazon\'s Echo Show speakers being able to play YouTube videos in September, on the basis that the retailer had altered the way the software worked. The version Amazon presented had lacked next video recommendations, subscriptions and other features - but these were restored in November, when Amazon made the device present a more normal view of YouTube. But, according to Techcrunch, the search firm believes its rights have still been violated because Amazon continues to overlay its own voice controls. Amazon has responded, saying: "Echo Show and Fire TV now display a standard web view of YouTube.com and point customers directly to YouTube\'s existing website. Google is setting a disappointing precedent by selectively blocking customer access to an open website. We hope to resolve this with Google as soon as possible." The dispute disadvantages consumers in two ways. Users will be unable to access a service that Amazon\'s devices had promised to deliver. And Amazon\'s refusal to even allow third-parties to sell certain Google products via its site makes it harder to find them at their lowest price. "It\'s a surprising turn of events in both respects," commented Ben Wood from the CCS Insight tech consultancy. "YouTube is all about maximising the number of people who see its content, and Amazon wants to be the so-called \'everything store\'It\'s all very unfortunate for consumers, who will have little understanding of the commercial tensions between the two companies. "I wonder whether the next step might be the intervention of a regulator to investigate whether they are behaving anti-competitively.')