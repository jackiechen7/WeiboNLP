# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import gzip
import marshal
from math import log, exp

from ..utils.frequency import AddOneProb


class Bayes(object):

    def __init__(self):
        # 标签数据对象
        self.d = {}
        self.total = 0

    def save(self, fname, iszip=True):
        d = {}
        d['total'] = self.total
        d['d'] = {}
        for k, v in self.d.items():
            d['d'][k] = v.__dict__
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            marshal.dump(d, open(fname, 'wb'))
        else:
            f = gzip.open(fname, 'wb')
            f.write(marshal.dumps(d))
            f.close()

    def load(self, fname, iszip=True):
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            d = marshal.load(open(fname, 'rb'))
        else:
            try:
                f = gzip.open(fname, 'rb')
                d = marshal.loads(f.read())
            except IOError:
                f = open(fname, 'rb')
                d = marshal.loads(f.read())
            f.close()
        self.total = d['total']
        self.d = {}
        for k, v in d['d'].items():
            self.d[k] = AddOneProb()
            self.d[k].__dict__ = v

    # data[[‘pos_words after handle’,‘pos’]],
    # Self.d={‘pos’:{‘pos_words: appear_times’},’neg’:{‘neg_words’: appear_times }}
    def train(self, data):
        for d in data:
            # d[0]:分词的结果，list
            # d[1]:正/负样本的标记
            c = d[1]
            # 判断数据字典中是否有当前标签
            if c not in self.d:
                # 如果没有标签，加入标签
                self.d[c] = AddOneProb()  # 类的初始化 双层嵌套字典
            # d[0]是评论的分词list，遍历分词list
            for word in d[0]:
                # 调用AddOneProb中的add方法，在c标签下添加单词和出现次数
                self.d[c].add(word, 1)
        # sum(map())表达式所求为正向词汇和负向词汇所有单词出现总和 Getsum表示的是pos/neg_word出现总次数。
        # 做函数映射 d.keys()为d[x]中x
        self.total = sum(map(lambda x: self.d[x].getsum(), self.d.keys()))

    def classify(self, x):
        # Self.d={‘pos’:{‘pos_words: appear_times’},’neg’:{‘neg_words’: appear_times }}
        tmp = {}
        # tmp = {‘pos’:log(p(x | c1) * p(c1)),’neg’:log(p(x | c2) * p(c2))}
        for k in self.d:  # k为‘pos’，‘neg’
            # tmp[1] = C1
            tmp[k] = log(self.d[k].getsum()) - log(self.total)
            for word in x:
                # tmp[c1] = p(c1) * p{x1 | c1} * p{x2 | c1}....->p(x | c1) *p(c1)
                tmp[k] += log(self.d[k].freq(word))
        ret, prob = 0, 0
        # 函数归一化，统计学相关计算
        for k in self.d:  # 分别计算积极类/消极类 对应的概率
            now = 0  # 代表在输入的文字语句中，每个字的特点都是一个类型 k的类型。
            try:
                for otherk in self.d:
                    now += exp(tmp[otherk]-tmp[k])  # 朴素贝叶斯二分类公式中的分母
                now = 1/now  # 取倒数
            except OverflowError:
                now = 0  # 词频为0，则取0
            if now > prob:
                ret, prob = k, now  # 若本次计算出的概率 > 原先概率，则词性ret = k, 概率 = now
        return ret, prob
