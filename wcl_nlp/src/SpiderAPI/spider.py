# -*- encoding: utf-8 -*-
"""
@FileName：spider.py\n
@Description：\n
@Author：wcl\n
@Time：2022/4/9 16:30\n
@Department：毕业设计
@Copyright：wcl
"""
import re
import requests
import traceback
import sys
import random
import time
import js2xml
import json
import urllib
import os

from os import path
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
from lxml import etree
from src.SnowNLPAPI.snownlp import SnowNLP
from src.SnowNLPAPI.snownlp import sentiment
# 个人，微博，评论信息
from .models import UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo
from .agents import getAgent


class Weibo:
    # Weibo类初始化
    def __init__(self, user_id, cookie, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字
        self.cookie = cookie  # 设置cookie
        self.filter = filter  # 取值范围为0或1 默认为0，代表爬取全部微博，1爬取用户的原创微博
        self.agent = getAgent()  # 获取访问网页的agent
        self.tweets_list_to_insert = list()
        self.comment_list_to_insert = list()

    def getTest(self):
        print(self.agent)
        return self.agent

    # 获取用户信息
    def get_userInfo(self):
        # noinspection PyBroadException
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie, headers=self.agent).content
            selector = etree.HTML(html)
            info = ";".join(selector.xpath('body/div[@class="c"]//text()'))  # 获取所有文本
            # 获取用户基本信息
            nickname = re.findall('昵称[：:]?(.*?);', info)  # 正则表达式，冒号后面的内容
            image = selector.xpath('body/div[@class="c"]//img/@src')
            gender = re.findall('性别[：:]?(.*?);', info)
            place = re.findall('地区[：:]?(.*?);', info)
            briefIntroduction = re.findall('简介[：:]?(.*?);', info)
            birthday = re.findall('生日[：:]?(.*?);', info)
            sexOrientation = re.findall('性取向[：:]?(.*?);', info)
            sentiment = re.findall('感情状况[：:]?(.*?);', info)
            vipLevel = re.findall('会员等级[：:]?(.*?);', info)
            authentication = re.findall('认证[：:]?(.*?);', info)
            url = re.findall('互联网[：:]?(.*?);', info)
            # 实例化
            user_info = UserInfo()  # models中的用户信息
            user_info._id = self.user_id
            if image:
                user_info.Image = image
            if nickname and nickname[0]:
                user_info.NickName = nickname[0].replace(u"\xa0", "")  # 替换不间断空白符
            if gender and gender[0]:
                user_info.Gender = gender[0].replace(u"\xa0", "")
            if place and place[0]:
                place = place[0].replace(u"\xa0", "").split(" ")
                user_info.Province = place[0]
                if len(place) > 1:
                    user_info.City = place[1]
            if briefIntroduction and briefIntroduction[0]:
                user_info.BriefIntroduction = briefIntroduction[0].replace(u"\xa0", "")
            if birthday and birthday[0]:
                # noinspection PyBroadException
                # 关闭错误类型报错
                try:
                    birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                    user_info.Birthday = birthday - datetime.timedelta(hours=8)  # 生日时间减去8小时
                except Exception:
                    user_info.Constellation = birthday[0]  # 可能是星座
            if sexOrientation and sexOrientation[0]:
                if sexOrientation[0].replace(u"\xa0", "") == gender[0]:
                    user_info.SexOrientation = "同性恋"
                else:
                    user_info.SexOrientation = "异性恋"
            if sentiment and sentiment[0]:
                user_info.Sentiment = sentiment[0].replace(u"\xa0", "")
            if vipLevel and vipLevel[0]:
                user_info.VIPlevel = vipLevel[0].replace(u"\xa0", "")
            if url:
                user_info.URL = url[0]

            #  微博粉丝等
            # noinspection PyBroadException
            try:
                urlothers = "https://weibo.cn/attgroup/opening?uid=%d" % (self.user_id)
                r = requests.get(urlothers, headers=self.agent, cookies=self.cookie)
                if r.status_code == 200:
                    selector = etree.HTML(r.content)
                    texts = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
                    if texts:
                        num_tweets = re.findall('微博\[(\d+)\]', texts)
                        num_follows = re.findall('关注\[(\d+)\]', texts)
                        num_fans = re.findall('粉丝\[(\d+)\]', texts)
                        # 如果存在就给user类
                        if num_tweets:
                            user_info.Num_Tweets = int(num_tweets[0])
                        if num_follows:
                            user_info.Num_Follows = int(num_follows[0])
                        if num_fans:
                            user_info.Num_Fans = int(num_fans[0])
            except Exception as e:
                pass

            try:
                UserInfo.objects.get(_id=self.user_id)
                return "用户数据已存在！"
            except UserInfo.DoesNotExist:
                user_info.save()
                return "用户信息爬取成功~"

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()  # 输出异常信息

    # 获取长微博全部文字内容
    def get_long_weibo(self, weibo_link):
        # noinspection PyBroadException
        try:
            html = requests.get(weibo_link, headers=self.agent, cookies=self.cookie).content
            selector = etree.HTML(html)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = info.xpath('//div[@id="M_"]//span[@class="ctt"]')[0].xpath(
                "string(.)").replace(u"\u200b", "").encode(sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            return wb_content

        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取转发微博信息
    def get_retweet(self, is_retweet, info, wb_content):
        # noinspection PyBroadException
        try:
            original_user = is_retweet[0].xpath("a/text()")
            retweet_reason = info.xpath("div")[-1].xpath("string(.)").replace(u"\u200b", "").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            retweet_reason = retweet_reason[:retweet_reason.rindex(u"赞")]

            if not original_user:
                wb_content = u"转发微博已被删除"
                if retweet_reason:
                    wb_content = (retweet_reason + "\n" + wb_content)
                return wb_content
            else:
                original_user = original_user[0]
            wb_content = (retweet_reason + "\n" + u"原始用户:" +
                          original_user + "\n" + u"转发内容:" + wb_content)
            return wb_content


        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博内容、
    def get_weibo_content(self, info):
        # noinspection PyBroadException
        try:
            str_t = info.xpath("div/span[@class='ctt']")
            weibo_content = str_t[0].xpath("string(.)").replace(u"\u200b", "").encode(
                sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            weibo_id = info.xpath("@id")[0][2:]
            a_link = info.xpath("div/span[@class='ctt']/a")  # 原始微博
            is_retweet = info.xpath("div/span[@class='cmt']")  # 转发微博
            if a_link:
                if a_link[-1].xpath("text()")[0] == u"全文":
                    weibo_link = "https://weibo.cn/comment/" + weibo_id
                    wb_content = self.get_long_weibo(weibo_link)
                    if wb_content:
                        if not is_retweet:
                            wb_content = wb_content[1:]
                        weibo_content = wb_content
            if is_retweet:  # 转发微博内容
                weibo_content = self.get_retweet(
                    is_retweet, info, weibo_content)
            return weibo_content



        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博发布位置
    def get_weibo_place(self, info):
        try:
            div_first = info.xpath("div")[0]
            a_list = div_first.xpath("a")
            weibo_place = u"无"
            for a in a_list:
                if ("place.weibo.com" in a.xpath("@href")[0] and
                        a.xpath("text()")[0] == u"显示地图"):
                    weibo_a = div_first.xpath("span[@class='ctt']/a")
                    if len(weibo_a) >= 1:
                        weibo_place = weibo_a[-1]
                        if u"的秒拍视频" in div_first.xpath("span[@class='ctt']/a/text()")[-1]:
                            if len(weibo_a) >= 2:
                                weibo_place = weibo_a[-2]
                            else:
                                weibo_place = u"无"
                        weibo_place = weibo_place.xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        break
            return weibo_place
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博发布时间
    def get_publish_time(self, info):
        # noinspection PyBroadException
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = str_time[0].xpath("string(.)").encode(
                sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
            publish_time = str_time.split(u'来自')[0].strip()
            if u"刚刚" in publish_time:
                publish_time = datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M')
            elif u"分钟" in publish_time:
                minute = publish_time[:publish_time.find(u"分钟")]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.datetime.now() - minute).strftime(
                    "%Y-%m-%d %H:%M")
            elif u"今天" in publish_time:
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                time = publish_time[3:]
                publish_time = today + " " + time
                # now_time = datetime.now()
                # publish_time = publish_time.replace('今天', now_time.strftime('%Y-%m-%d'))
            elif u"月" in publish_time:
                year = datetime.datetime.now().strftime("%Y")
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = (year + "-" + month + "-" + day + " " + time)
                # now_time = datetime.now()
                # time_string = publish_time.replace('月', '-').replace('日', '')
                # time_string = str(now_time.year) + '-' + time_string
                # publish_time = time_string
            else:
                publish_time = publish_time[:16]
            return publish_time
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博发布工具
    def get_publish_tool(self, info):
        # noinspection PyBroadException
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = str_time[0].xpath("string(.)").encode(
                sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
            if len(str_time.split(u'来自')) > 1:
                publish_tool = str_time.split(u'来自')[1]
            else:
                publish_tool = u"无"
            return publish_tool
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    # 获取微博用户信息
    """
    以上六个函数都为获取微博用户信息服务
    """

    def get_weibo_info(self):
        # noinspection PyBroadException
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter
            )
            html = requests.get(url, cookies=self.cookie, headers=self.agent).content
            selector = etree.HTML(html)
            if not selector.xpath("//input[@name='mp']"):  # 判断是否为第一页
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"  # 匹配字符中连续的字符串
            print(page_num)
            for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, headers=self.agent, cookies=self.cookie).content
                selector2 = etree.HTML(html2)
                infos = selector2.xpath("//div[@class='c' and @id]")
                print(infos)
                info_s = selector2.xpath("//div[@class='c']")
                is_empty = info_s[0].xpath("div/span[@class='ctt']")
                if is_empty:  # 判断是否有微博
                    for info in infos:
                        tweetsItems = TweetsInfo()
                        tweetsItems.UserInfo_id = self.user_id  # 微博ID
                        wb_id = info.xpath("@id")
                        print('保存前wb_id', wb_id)
                        # 微博内容
                        content = self.get_weibo_content(info)
                        # 微博位置
                        cooridinates = self.get_weibo_place(info)
                        # 微博发布时间
                        pubtime = self.get_publish_time(info)
                        # 微博发布工具
                        tools = self.get_publish_tool(info)
                        print('保存前', tools)

                        str_footer = info.xpath("div")[-1]  # 倒数第一个DIV
                        str_footer = str_footer.xpath("string(.)").encode(  # string(.)比text()更好，因为他可以合成并且拼接字符串
                            sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
                        str_footer = str_footer[str_footer.rfind(u'赞'):]  # 冒号  最后出现的位置匹配到最后的所有字符串
                        guid = re.findall(pattern, str_footer, re.M)
                        # 点赞数
                        like = int(guid[0])
                        # 转发数
                        transfer = int(guid[1])
                        # 评论数
                        comment = int(guid[2])

                        if wb_id:
                            tweetsItems._id = wb_id[0]
                        if content:
                            tweetsItems.Content = content
                            s = SnowNLP(
                                content.replace('转发理由', '').replace('转发内容', '').replace('原始用户', '').replace('转发微博已被删除',
                                                                                                            ''))
                            mm = ()
                            for i in s.tags:
                                mm += i
                            tweetsItems.tags = s.keywords(5)
                            tweetsItems.pinyin = mm
                            tweetsItems.sentiments = str(s.sentiments)
                            print(s.keywords(5))
                        if cooridinates:
                            tweetsItems.Co_oridinates = cooridinates
                        if like:
                            tweetsItems.Like = like
                        if transfer:
                            tweetsItems.Transfer = transfer
                        if comment:
                            tweetsItems.Comment = comment
                        if pubtime:
                            tweetsItems.PubTime = pubtime
                        if tools:
                            tweetsItems.Tools = tools
                        try:
                            TweetsInfo.objects.get(_id=tweetsItems._id)
                        except TweetsInfo.DoesNotExist:
                            print(tweetsItems)
                            tweetsItems.save()
        except Exception as e:
            print("Error微博文本: ", e)
            traceback.print_exc()

    def fix_time(self, publish_time):
        dd = datetime.datetime.strptime(publish_time, '%a %b %d %H:%M:%S %z %Y')  # 解析为时间元组
        publish_time = dd.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
        return publish_time

    def time_fix(self, time_string):
        now_time = datetime.datetime.now()
        if '刚刚' in time_string:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        if '分钟前' in time_string:
            minutes = re.search(r'^(\d+)分钟', time_string).group(1)
            created_at = now_time - timedelta(minutes=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M:%S')

        if '小时前' in time_string:
            minutes = re.search(r'^(\d+)小时', time_string).group(1)
            created_at = now_time - timedelta(hours=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M:%S')

        if '今天' in time_string:
            return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

        if '昨天' in time_string:
            created_at = now_time + timedelta(days=int(-1))
            return time_string.replace('昨天', created_at.strftime('%Y-%m-%d'))

        if '月' in time_string:
            time_string = time_string.replace('月', '-').replace('日', '')
            time_string = str(now_time.year) + '-' + time_string
            return time_string

        if '-' in time_string:
            time_string = str(now_time.year) + '-' + time_string
            return time_string

        return time_string

    # 获取微博评论信息
    def get_comment_info(self, id):
        c_urls = 'https://m.weibo.cn/api/comments/show?id=' + id + '&page={}'
        wb_url = 'https://m.weibo.cn/detail/' + id
        wb_r = requests.get(wb_url, headers=self.agent, cookies=self.cookie).content
        soup = BeautifulSoup(wb_r, 'lxml')
        src = soup.select('body script')[0].string
        src_text = js2xml.parse(src, debug=False)  # 处理转义字符
        src_tree = js2xml.pretty_print(src_text)
        selector2 = etree.HTML(src_tree)
        # 基本信息
        wb_id = selector2.xpath("//property[@name='id']//text()")[1]
        wb_userName = selector2.xpath("//property[@name='screen_name']/string//text()")[0]
        wb_userId = selector2.xpath("//property[@name='profile_url']//text()")[1].split('uid=')[1]
        wb_userId = wb_userId[0:10]   # 只有前10位才是ID
        wb_user_profile_image_url = selector2.xpath("//property[@name='profile_image_url']//text()")[1]
        wb_created_at = selector2.xpath("//property[@name='created_at']//text()")[1]
        wb_source = selector2.xpath("//property[@name='source']//text()")[1]
        wb_text = selector2.xpath("//property[@name='text']//text()")[1]
        wb_pic_ids = selector2.xpath("//property[@name='pic_ids']/array/string//text()")
        wb_reposts = selector2.xpath("//property[@name='reposts_count']//@value")[0]
        wb_comments = selector2.xpath("//property[@name='comments_count']//@value")[0]
        wb_like = selector2.xpath("//property[@name='attitudes_count']//@value")[0]

        commentWeiboInfo = CommentWeiboInfo()
        if wb_id:
            commentWeiboInfo.wb_id = wb_id
        if wb_userName:
            commentWeiboInfo.wb_userName = wb_userName
        if wb_userId:
            commentWeiboInfo.wb_userId = wb_userId
        if wb_user_profile_image_url:
            commentWeiboInfo.wb_user_profile_image_url = wb_user_profile_image_url
        if wb_created_at:
            commentWeiboInfo.wb_created_at = self.fix_time(wb_created_at)
        if wb_source:
            commentWeiboInfo.wb_source = wb_source
        if wb_text:
            commentWeiboInfo.wb_text = wb_text
        if wb_pic_ids:
            commentWeiboInfo.wb_pic_ids = wb_pic_ids
            filepath = path.abspath(path.join(os.getcwd(), "webview/static"))
            print(filepath)
            for wb_pic_id in wb_pic_ids:
                with urllib.request.urlopen("https://wx2.sinaimg.cn/large/" + wb_pic_id, timeout=30) as response, open(
                        filepath + "\\" + wb_pic_id + ".jpg", 'wb') as f_save:
                    print("下载图片%s" % wb_pic_id)
                    f_save.write(response.read())
                    f_save.flush()
                    f_save.close()
        if wb_reposts:
            commentWeiboInfo.wb_reposts = int(wb_reposts)
        if wb_comments:
            commentWeiboInfo.wb_comments = int(wb_comments)
        if wb_like:
            commentWeiboInfo.wb_like = int(wb_like)

        try:
            CommentWeiboInfo.objects.get(wb_id=commentWeiboInfo.wb_id)
            print("微博内容已存在数据库")
        except CommentWeiboInfo.DoesNotExist:
            print("微博内容抓取完毕，开始写入数据库")
            commentWeiboInfo.save()
            self.tweets_list_to_insert.append(commentWeiboInfo)
            # CommentWeiboInfo.objects.bulk_create(self.tweets_list_to_insert)
            print("微博内容写入数据库成功,开始抓取评论")
        except Exception as e:
            return "e:", e

        i = 1
        comment_num = 1
        while True:
            r = requests.get(url=c_urls.format(i), headers=self.agent, cookies=self.cookie)
            if int(r.json()['ok']) == 1:
                comment_data = r.json()['data']['data']
                print('正在读取第 %s 页评论：' % i)
                for j in range(0, len(comment_data)):
                    commentInfo = CommentInfo()
                    print('第 %s 条评论' % comment_num)
                    user = comment_data[j]
                    wb_id = id
                    # 评论用户
                    c_id = user['id']
                    c_created_at = user['created_at']
                    c_source = re.sub('[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '', user['source'])
                    c_user_id = user['user']['id']
                    c_user_name = user['user']['screen_name']
                    c_user_img = user['user']['profile_image_url']
                    c_user_url = user['user']['profile_url']
                    c_text = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '',
                                    user['text'])
                    c_likenum = user['like_counts']
                    if wb_id:
                        commentInfo.CommentWeiboInfo_id = wb_id
                    if c_id:
                        commentInfo.c_id = c_id
                    if c_created_at:
                        commentInfo.c_created_at = self.time_fix(c_created_at)
                    if c_source:
                        commentInfo.c_source = c_source
                    if c_user_id:
                        commentInfo.c_userId = c_user_id
                    if c_user_name:
                        commentInfo.c_user_name = c_user_name
                    if c_user_img:
                        commentInfo.C_profile_image_url = c_user_img
                    if c_user_url:
                        commentInfo.C_profile_url = c_user_url
                    if c_text:
                        commentInfo.c_text = c_text
                    if c_likenum:
                        commentInfo.c_like_num = int(c_likenum)
                    comment_num += 1
                    try:
                        CommentInfo.objects.get(c_id=commentInfo.c_id)
                        print("评论已存在数据库")
                    except CommentInfo.DoesNotExist:
                        self.comment_list_to_insert.append(commentInfo)
                        print(len(self.comment_list_to_insert))
                i += 1
                time.sleep(2)
            else:
                print("跳出while=======================")
                break
        try:
            print("评论抓取完毕，开始写入数据库")
            CommentInfo.objects.bulk_create(self.comment_list_to_insert) # 批量导入
            print("评论写入数据库成功")
            return "数据抓取完毕"
        except Exception as e:
            return "e:", e
