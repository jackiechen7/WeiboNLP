from django.test import TestCase

# Create your tests here.
from collections import Counter
from src.ScrapydAPI.models import Target, UserInfo, TweetsInfo

targets = Target.objects.values("uid", "group")
print(targets)