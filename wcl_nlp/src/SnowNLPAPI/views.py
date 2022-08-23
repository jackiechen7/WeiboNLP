from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from .snownlp import SnowNLP
from .snownlp import sentiment
# Create your views here.
# 正则表达式
import re
import requests


class SnowNLPWeibo:
    def SnowNLPAPI(request):
        if request.method == "GET":
            text = request.GET.get("snownlp")
            print(text)
        s = SnowNLP(text)
        result = {}
        # set无序不重复的数据集
        myset = set()
        # 正则表达式：表示找到不是汉字也不是字母的字符
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z]")
        # sub函数替换text中正则表达式内容为空
        text = cop.sub('', text)
        for ch in text:
            if ch in myset:
                pass
            else:
                myset.add(ch)
        # myset中字符在text文本中出现的次数 ch对应的数字
        for ch in myset:
            result[ch] = text.count(ch)
        # .items为字典,对字典第二个元素排列（数字）
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        mm = {
            'sentiments': s.sentiments,  # 乐观的概率
            'keywords': s.keywords(3),  # 句子关键词
            'tf': result,
            'words': s.words,  # 进行分词
            'sentences': s.sentences,  # 断句
            'tf2': s.tf,  # 词频
            'idf': s.idf,  # 逆文档频率
        }
        return JsonResponse(mm)
