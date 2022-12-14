# Generated by Django 2.2 on 2022-04-12 21:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='评论的ID')),
                ('comment_user_id', models.CharField(max_length=50, verbose_name='评论的用户ID')),
                ('weibo_url', models.TextField(blank=True, verbose_name='weibo的URL')),
                ('content', models.TextField(blank=True, verbose_name='评论内容')),
                ('created_at', models.CharField(blank=True, max_length=30, verbose_name='评论创建时间')),
                ('crawl_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '评论内容',
                'verbose_name_plural': '评论内容',
            },
        ),
        migrations.CreateModel(
            name='RelationshipsInfo',
            fields=[
                ('_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='用户关系ID')),
                ('fan_id', models.CharField(max_length=50, verbose_name='关注者的用户ID')),
                ('followed_id', models.CharField(max_length=50, verbose_name='被关注者的用户ID')),
                ('crawl_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户关系',
                'verbose_name_plural': '用户关系',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20, verbose_name='爬取用户')),
                ('cookie', models.TextField(verbose_name='设置cookie')),
                ('isScrapy', models.IntegerField(default=0, verbose_name='是否爬取')),
                ('group', models.IntegerField(default=0, verbose_name='用户分组')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '爬虫初始',
                'verbose_name_plural': '爬虫初始',
            },
        ),
        migrations.CreateModel(
            name='TweetsInfo',
            fields=[
                ('_id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='微博ID')),
                ('user_id', models.CharField(max_length=200, verbose_name='用户信息')),
                ('content', models.TextField(verbose_name='微博内容')),
                ('created_at', models.DateTimeField(blank=True, verbose_name='发表时间')),
                ('weibo_url', models.TextField(blank=True, verbose_name='weibo的URL')),
                ('like_num', models.IntegerField(blank=True, default=0, verbose_name='点赞数')),
                ('comment_num', models.IntegerField(blank=True, default=0, verbose_name='评论数')),
                ('repost_num', models.IntegerField(blank=True, default=0, verbose_name='转载数')),
                ('crawl_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '微博信息',
                'verbose_name_plural': '微博信息',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('_id', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='用户id')),
                ('Image', models.TextField(blank=True, verbose_name='用户头像')),
                ('nick_name', models.CharField(max_length=30, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', max_length=6, verbose_name='性别')),
                ('labels', models.CharField(blank=True, max_length=500, verbose_name='标签')),
                ('province', models.CharField(blank=True, max_length=30, verbose_name='所在省')),
                ('city', models.CharField(blank=True, max_length=30, verbose_name='所在城市')),
                ('brief_introduction', models.CharField(blank=True, max_length=500, verbose_name='简介')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('constellation', models.CharField(blank=True, max_length=30, verbose_name='星座')),
                ('tweets_num', models.IntegerField(default=0, verbose_name='微博数')),
                ('fans_num', models.IntegerField(default=0, verbose_name='关注数')),
                ('follows_num', models.IntegerField(blank=True, default=0, verbose_name='粉丝数')),
                ('sex_orientation', models.CharField(blank=True, max_length=30, verbose_name='性取向')),
                ('sentiment', models.CharField(blank=True, max_length=30, verbose_name='感情状况')),
                ('vip_level', models.CharField(blank=True, max_length=30, verbose_name='会员等级')),
                ('authentication', models.CharField(blank=True, max_length=30, verbose_name='认证')),
                ('person_url', models.CharField(blank=True, max_length=30, verbose_name='首页链接')),
                ('crawl_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
