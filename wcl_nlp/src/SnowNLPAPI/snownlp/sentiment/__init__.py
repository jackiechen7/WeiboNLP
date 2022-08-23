# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import codecs

from .. import normal
from .. import seg
from ..classification.bayes import Bayes

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'sentiment.marshal')


class Sentiment(object):

    def __init__(self):
        self.classifier = Bayes()  # 使用Bayes模型

    def save(self, fname, iszip=True):
        self.classifier.save(fname, iszip)  # 保存最终模型

    def load(self, fname=data_path, iszip=True):
        self.classifier.load(fname, iszip)  # 加载贝叶斯模型

    def handle(self, doc):
        words = seg.seg(doc)  # 分词
        words = normal.filter_stop(words)  # 去停用词
        return words   # 返回分词结果

    def train(self, neg_docs, pos_docs):  # 训练
        data = []
        # 读入负样本
        for sent in neg_docs:
            data.append([self.handle(sent), 'neg'])
        # 读入正样本
        for sent in pos_docs:
            # data[[‘pos_words after handle’,‘pos’]
            data.append([self.handle(sent), 'pos'])
        # 调用贝叶斯模型训练方法
        self.classifier.train(data)

    def classify(self, sent):  # 预测
        # 调用sentiment类中的Handel方法
        # 调用Bayes中的classify 方法
        ret, prob = self.classifier.classify(self.handle(sent))
        if ret == 'pos':
            return prob
        return 1-prob


classifier = Sentiment()
classifier.load()  # 运行sentiment时要进行读取操作


def train(neg_file, pos_file):

    neg_docs = codecs.open(neg_file, 'r', 'utf-8').readlines()
    pos_docs = codecs.open(pos_file, 'r', 'utf-8').readlines()
    global classifier
    classifier = Sentiment()  # 实例化Sentiment
    classifier.train(neg_docs, pos_docs)


def save(fname, iszip=True):
    classifier.save(fname, iszip)


def load(fname, iszip=True):
    classifier.load(fname, iszip)


def classify(sent):
    return classifier.classify(sent)
