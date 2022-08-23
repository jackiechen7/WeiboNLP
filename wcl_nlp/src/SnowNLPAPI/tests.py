from collections import Counter

from django.test import TestCase

# Create your tests here.
# from snownlp import SnowNLP
# from snownlp import sentiment
# # Create your views here.
# text = '希望本无所谓有，也无所谓无，这就像地上的路，其实地上本没有路，走的人多了，也便成了路。'
# s = SnowNLP(text)
# # print(s.words)
# # print(s.sentences)
# # print(s.tf)
# # print(s.idf)
# # print(s.tags)
# print(s.keywords(5))
# mm = ()
# for i in s.tags:
#     mm += i
# print(mm)
list = [1, 2, 3, 2, 4, 3, 4, 1, 5]
c = Counter()
for word in list:
    c[word] += 1
print(c.items())

