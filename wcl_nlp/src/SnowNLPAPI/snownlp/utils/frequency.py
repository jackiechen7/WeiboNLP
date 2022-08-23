# -*- coding: utf-8 -*-

from . import good_turing

class BaseProb(object):
    # Self.d={‘pos’:{‘pos_words: appear_times’},’neg’:{‘neg_words’: appear_times }}
    def __init__(self):
        # 标签数据对象
        self.d = {}
        self.total = 0.0
        self.none = 0

    def exists(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def get(self, key):
        if not self.exists(key):
            return False, self.none
        # ‘pos_words: appear_times’
        return True, self.d[key]

    def freq(self, key):
        return float(self.get(key)[1])/self.total

    def samples(self):
        return self.d.keys()


class NormalProb(BaseProb):

    def add(self, key, value):
        if not self.exists(key):
            self.d[key] = 0
        self.d[key] += value
        self.total += value


class AddOneProb(BaseProb):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 1  # 默认所有的none为1

    # 这里如果value也等于1，则当key不存在时，累加的是2
    def add(self, key, value):
        self.total += value  # 单词数+1
        # 不存在该key时，需新建key
        if not self.exists(key):
            self.d[key] = 1  # 该单词在该标签出现次数为1
            self.total += 1  # 该标签单词总数+1
        self.d[key] += value  # 存在时单词在该标签出现次数再加1


class GoodTuringProb(BaseProb):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.handled = False

    def add(self, key, value):
        if not self.exists(key):
            self.d[key] = 0
        self.d[key] += value

    def get(self, key):
        if not self.handled:
            self.handled = True
            tmp, self.d = good_turing.main(self.d)
            self.none = tmp
            self.total = sum(self.d.values())+0.0
        if not self.exists(key):
            return False, self.none
        return True, self.d[key]
