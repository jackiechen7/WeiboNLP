import sys

from django.test import TestCase

# Create your tests here.
# from datetime import datetime,date,timedelta
# now = datetime.now();
# nextDay = now + timedelta(days = 1);#增加一天后的时间
# nextSecond = now + timedelta(seconds = 1);#增加一秒后的时间
# span  = now - nextDay;#获取时间差对象
# print(now);
# print(nextDay);
# print(nextSecond);
# print(span.total_seconds());#获取时间差 以秒为单位

from bs4 import BeautifulSoup
import js2xml
import requests
import re
from lxml import etree


if __name__ == '__main__':
    url = 'https://weibo.cn/u/5094308006?filter=1&page=1'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.84 Safari/537.36 ',
    }
    cookies = {
        'cookie': 'SCF=AlDTm9aRFhxgZlXC8ZEwn5ElPOcp6IjFPTHzRMbpDMnf3Ap9ZmR7Cl6touOtI7N-mrRZhmwOJSwDVZU7OysFLcc.; SUB=_2A25PVeylDeRhGeNI7VsY8y7Ewz-IHXVsufTtrDV6PUJbktB-LRL2kW1NSClw4Y9MflL5rbQxirLlWDWtGvA3Or4l; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW0c4YkOsbcz.TRPuxRGBSj5NHD95QfSoq41Ke71hn0Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSKqc1K.0ehnRe7tt; _T_WM=a25aac17d8e69ba38c6da422581b2e6c; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4755399473627964%26luicode%3D20000061%26lfid%3D4755399473627964; _T_WL=1; _WEIBO_UID=5669930883',
    }
    html = requests.get(url, cookies=cookies, headers=headers).content
    selector = etree.HTML(html)
    if not selector.xpath("//input[@name='mp']"):  # 判断是否为第一页
        page_num = 1
    else:
        page_num = (int)(selector.xpath(
            "//input[@name='mp']")[0].attrib["value"])
    print(page_num)
    pattern = r"\d+\.?\d*"  # 匹配字符中连续的字符串
    for page in range(1, page_num + 1):
        url2 = "https://weibo.cn/u/5094308006?filter=1&page=%d" % page
        html2 = requests.get(url2, headers=headers, cookies=cookies).content
        selector2 = etree.HTML(html2)
        infos = selector2.xpath("//div[@class='c' and @id]")
        # print(infos)
        info_s = selector2.xpath("//div[@class='c']")
        is_empty = info_s[0].xpath("div/span[@class='ctt']")
        if is_empty:  # 判断是否有微博
            for info in infos:
                # tweetsItems = TweetsInfo()
                # tweetsItems.UserInfo_id = self.user_id  # 微博ID
                wb_id = info.xpath("@id")
                str_footer = info.xpath("div")[-1]  # 倒数第一个DIV
                str_footer = str_footer.xpath("string(.)").encode(  # string(.)比text()更好，因为他可以合成并且拼接字符串
                    sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                str_footer = str_footer[str_footer.rfind(u'赞'):]  # 冒号  最后出现的位置匹配到最后的所有字符串
                guid = re.findall(pattern, str_footer, re.M)
                print(guid)



