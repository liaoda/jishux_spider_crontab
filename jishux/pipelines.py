# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
<<<<<<< HEAD
from urllib.parse import urljoin
=======
>>>>>>> 1e63ef31bf023ca74d60f3194e6b2f993c0e7599
import re
from urllib.parse import urljoin
from urllib.parse import urlparse

import pymysql
import scrapy
from scrapy.pipelines.images import FilesPipeline

<<<<<<< HEAD
# from jishux.misc.qiniu_tools import upload_file as qiniu_upload
from jishux.misc.aliyunoss_tools import upload_file as ali_upload
=======
# from jishux.misc.aliyunoss_tools import upload_file as ali_upload
>>>>>>> 1e63ef31bf023ca74d60f3194e6b2f993c0e7599
import jishux.settings as settings
from jishux.items import JishuxItem
from jishux.misc.all_secret_set import mysql_config
from jishux.misc.qiniu_tools import upload_file as qiniu_upload
from .misc.utils import get_post_type_id


class JishuxPipeline(object):
    def process_item(self, item, spider):
        return item


class UrlSpiderPipeline(object):
    def __init__(self):
        self.all_item = {}

    def process_item(self, item, spider):
        self.all_item[item['site_url']] = item['site_type']
        return item

    def close_spider(self, spider):
        all_item_str = str(self.all_item)
        with open('name_map_params.py', 'w') as f:
            f.write('urls_dict = ' + all_item_str)


class JishuxDataCleaningPipeline(object):
    '''
    数据清洗pipeline
    '''

    def process_item(self, item, spider):
        item['content_html'] = self.clean_tags(item['content_html'])
        # print(item['content_html'])
        return item

    def clean_tags(self, content_html):
        '''
        加工标签
        '''
        # nofollow
        content_html = content_html.replace('<a', '<a rel="nofollow"')
        # 空白符的处理
        content_html = content_html.strip().replace('\r', '').replace('\n', '').replace('\t', '')
        p1 = re.compile('<p>(\s*|<br>|<br/>|&nbsp;)</p>')
        content_html = re.sub(p1, '', content_html)
        # TODO: 代码标签统一处理

        return content_html

    def clean_ads(self, item):
        '''
        清洗广告
        '''
        return item


class JISHUXFilePipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        print(results)
        content = item['content_html']
        image_paths = []
        for x in results:
            if x[0]:
                path = self.pre_item(settings.FILES_STORE + x[1]['path'])
                if path is None:
                    print('上传失败')
                else:
                    image_paths.append(path)
                    content = content.replace(x[1]['url'], path)
                    relative_path = urlparse(x[1]['url']).path
                    content = content.replace('..' + relative_path, path)  # todo 非bigdata 注释掉
                    content = content.replace(relative_path, path)
                    content = content.replace('../../pic/pm.jpg',
                                              'http://wercoder.com/dedemao/images/logo.png')  # todo 非bigdata 注释掉
        item['litpic'] = image_paths[0] if len(image_paths) > 0 else ''
        item['content_html'] = content
        return item

    def get_media_requests(self, item, info):
        if item['image_urls']:
            for image_url in item['image_urls']:
                image_url = urljoin(item['post_url'], image_url)
                yield scrapy.Request(image_url, headers={'Referer': item['post_url']})

    def pre_item(self, path):
        return qiniu_upload(path, path.split('/')[-1])


# class JishuxReplaceImagePipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         if item['image_urls']:
#             for image_url in item['image_urls']:
#                 image_url = urljoin(item['post_url'], image_url)
#                 yield scrapy.Request(image_url)
#
#
#     def item_completed(self, results, item, info):
#         content = item['content_html']
#         image_paths = []
#         for x in results:
#             if x[0]:
#                 path = self.pre_item(settings.IMAGES_STORE + x[1]['path'])
#                 if path is None:
#                     print('上传失败')
#                 else:
#                     image_paths.append(path)
#                     content = content.replace(x[1]['url'], path)
#                     relative_path = urlparse(x[1]['url']).path
#                     content = content.replace('..' + relative_path, path)  # todo 非bigdata 注释掉
#                     content = content.replace(relative_path, path)
#                     content = content.replace('../../pic/pm.jpg',
#                                               'http://wercoder.com/dedemao/images/logo.png')  # todo 非bigdata 注释掉
#         item['litpic'] = image_paths[0] if len(image_paths) > 0 else ''
#         item['content_html'] = content
#         return item
#
#     def file_path(self, request, response=None, info=None):
#         url = request.url
#         image_guid = hashlib.sha1(to_bytes(url)).hexdigest()
#         suffix = url.split('.')[-1]
#         if suffix not in ['jpg', 'jpeg', 'gif', 'png', 'JPG', 'JPEG', 'GIF', 'PNG']:
#             suffix = 'jpg'
#         return 'full/%s.%s' % (image_guid, suffix)
#
#     # 图片下载上传到七牛,重新拼接img
#     def pre_item(self, path):
#         return qiniu_upload(path, path.split('/')[-1])


class JishuxMysqlPipeline(object):
    def __init__(self):
        # 创建连接git l
        self.connection = pymysql.connect(**mysql_config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):

        if isinstance(item, JishuxItem):
            # print(item)
            # pass
            self.insert_item(item)

    def insert_item(self, item):
        keywords = item['keywords']
        description = item['description'].replace("'", r"\'") if item['content_html'] else ''
        description = description.replace('"', r'\"') if description else ''
        content = item['content_html'].replace("'", r"\'") if item['content_html'] else ''
        content = content.replace('"', r'\"') if content else ''
        title = item['post_title'] if item['post_title'] else ''
        source = item['cn_name']
        article_type = 'p' if len(item['image_urls']) > 0 else ''
        author = '技术栈' if not item['author'] else item['author']
        litpic = item['litpic'] if item['litpic']else ''
        type_id = get_post_type_id(item['post_type'])
        crawl_time = str(item['crawl_time'])
        sql_insert_meta = 'INSERT INTO dede_archives (typeid, sortrank, flag, ismake, channel, title, writer, source, pubdate, senddate, mid, keywords, description, dutyadmin,voteid,litpic,click) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s","%s","%s")' % (
            type_id, crawl_time, article_type, -1, 1, title, author, source, crawl_time, crawl_time,
            1, keywords, description, 1, 0, litpic, random.randint(5000, 10000))
        self.cursor.execute(sql_insert_meta)
        sql_last_id = 'SELECT LAST_INSERT_ID()'
        self.cursor.execute(sql_last_id)
        a = self.cursor.fetchone()
        aid = a['LAST_INSERT_ID()']
        sql_insert_content = 'INSERT INTO dede_addonarticle (aid, typeid, body, userip) VALUES("%s","%s","%s","%s")' % (
            aid, type_id, content, '127.0.0.1')
        print(sql_insert_content)
        self.cursor.execute(sql_insert_content)
        sql_insert_arctiny = 'INSERT INTO dede_arctiny (id, typeid, channel, senddate, sortrank,mid) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (
            aid, type_id, 1, crawl_time, crawl_time, 1)
        self.cursor.execute(sql_insert_arctiny)
        for key in keywords.split(','):
            # 判断tag是否在tagindex中存在
            sql_find_tag_exist = 'SELECT * FROM dede_tagindex WHERE tag= "%s"' % key
            # 如果不存在插入tag_index '" + key + "'," + type_id + ",1," + crawl_time + "," + crawl_time + "," + crawl_time + "
            sql_insert_tag_index = 'INSERT INTO dede_tagindex (tag, typeid, total, weekup, monthup, addtime) VALUES ("%s","%s","%s","%s","%s","%s")' % (
                key, type_id, 1, crawl_time, crawl_time, crawl_time)
            # 如果存在则计数+1
            sql_update_count_add_1 = 'UPDATE dede_tagindex SET total=total+1  WHERE tag= "%s"' % key
            self.cursor.execute(sql_find_tag_exist)
            one = self.cursor.fetchone()

            if one:
                self.cursor.execute(sql_update_count_add_1)
                tid = one['id']
            else:
                self.cursor.execute(sql_insert_tag_index)
                self.cursor.execute(sql_last_id)
                last = self.cursor.fetchone()
                tid = last['LAST_INSERT_ID()']
            # 插入tag到taglist
            sql_insert_tag_list = 'INSERT INTO dede_taglist (tid, aid, arcrank, typeid, tag) VALUES ("%s", "%s", "%s", "%s", "%s")' % (
            str(tid), str(aid), 0, str(type_id), key)
            print(sql_insert_tag_list)
            self.cursor.execute(sql_insert_tag_list)

        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()
