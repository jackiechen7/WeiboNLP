# -*- coding: utf-8 -*-

# Scrapy settings for bot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wcl_nlp.settings'
sys.path.append(os.path.dirname(os.path.abspath('.')))

import django
django.setup()

import random
import pymysql.cursors
# 连接数据库
connect = pymysql.connect(
    host='localhost',  # 数据库地址
    port=3306,  # 数据库端口
    db='WclNlpSystem',  # 数据库名
    user='root',  # 数据库用户名
    passwd='178512',  # 数据库密码
    charset='utf8mb4',  # 编码方式
    use_unicode=True)
# 通过cursor执行增删查改
cursor = connect.cursor()
cursor.execute("""SELECT cookie from scrapydapi_target""")
cookie = cursor.fetchall()
connect.close()
cursor.close()
listCookie = []
for res1 in cookie:
    listCookie.append(res1)
random.shuffle(listCookie)

BOT_NAME = 'bot'

SPIDER_MODULES = ['bot.spiders']
NEWSPIDER_MODULE = 'bot.spiders'

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': '_T_WM=d84c5fcfd0f3c538f7724258d5ff0b01; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn; WEIBOCN_WM=3349; SCF=AtyveNC-2jwM8ZmxQna39T0Yk4Su6Qrn8mLXh5xm9EshuEPpvhDuS3lY36s4TkyuuxpT7keHpqlRnRZpUaQKN5Y.; SUB=_2A25PVQ6rDeRhGeNI7VsY8y7Ewz-IHXVsuZLjrDV6PUNbktAfLWX6kW1NSClw4SCJnn0LpRK4_0ik2kBod6c0pKqA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW0c4YkOsbcz.TRPuxRGBSj5JpX5KzhUgL.Fo-cSo.4e05R1he2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfSoq41Ke71hn0; SSOLoginState=1649508091; ALF=1652100091; MLOGIN=1; _T_WL=1; _WEIBO_UID=5669930883; M_WEIBOCN_PARAMS=luicode%3D20000174',
   }

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'bot.pipelines.BotPipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bot (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bot.middlewares.BotSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'bot.middlewares.BotDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'bot.pipelines.BotPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
