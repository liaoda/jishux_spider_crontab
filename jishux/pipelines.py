# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
from urllib.parse import urljoin, urlparse, urlsplit

import pymysql
from scrapy import Selector, Request
from scrapy.pipelines.images import FilesPipeline

import jishux.settings as settings
from jishux.misc.all_secret_set import mysql_config
from jishux.misc.qiniu_tools import upload_file as qiniu_upload
from .misc.clean_tools import clean_tags
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
        item = clean_tags(item)
        return item


class JISHUXFilePipeline(FilesPipeline):
    '''
    文件下载pipeline
    '''

    def get_media_requests(self, item, info):
        item['image_urls'] = Selector(text=item['content_html']).xpath('//img/@src').extract()
        if item['image_urls']:
            for image_url in item['image_urls']:
                if image_url.startswith('data:image'):
                    continue
                image_url = urljoin(item['post_url'], image_url)
                yield Request(image_url, headers={'Referer': "{0.scheme}://{0.netloc}/".format(urlsplit(image_url))})

    def item_completed(self, results, item, info):
        item['litpic'] = ''
        for x in results:
            if x[0]:
                # 上传
                local_path = settings.FILES_STORE + x[1]['path']
                qiniu_url = qiniu_upload(local_path, local_path.split('/')[-1])
                if qiniu_url:
                    # 文章封面图 litpic
                    if not item['litpic']:
                        item['litpic'] = qiniu_url

                    request_url = x[1]['url']
                    relative_path = urlparse(request_url).path
                    # 替换1：完全正常的
                    original_url = request_url
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换2：没有主机名的并且开头是/
                    original_url = relative_path
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换3：没有主机名并且开头没有/
                    original_url = relative_path[1:]
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换4：没有主机名并且开头是./
                    original_url = '.' + relative_path
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换5：没有主机名并且开头是../
                    original_url = '../' + relative_path.split(sep='/', maxsplit=2)[-1]
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换6：没有主机名并且开头是../../
                    original_url = '../../' + relative_path.split(sep='/', maxsplit=3)[-1]
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
                    # 替换7：没有http:或者https:协议的
                    if request_url.startswith('https'):
                        original_url = request_url[6:]
                    else:
                        original_url = request_url[5:]
                    if original_url in item['content_html']:
                        item['content_html'] = item['content_html'].replace(original_url, qiniu_url)
                        continue
        return item

class JishuxMysqlPipeline(object):
    def __init__(self):
        # 创建连接git l
        self.connection = pymysql.connect(**mysql_config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if item:
            self.insert_item(item)
        return item

    def insert_item(self, item):
        keywords = item['keywords']
        description = item['description'].replace('"', r'\"') if item['description'] else ''
        content = item['content_html'].replace('"', r'\"') if item['content_html'] else ''
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
        self.cursor.close()
        self.connection.close()
