# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

try:

    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
import random
import time
from urllib.parse import urljoin

import pymysql
import scrapy
from qiniu import Auth, put_file, etag
from scrapy.pipelines.images import ImagesPipeline

import jishux.misc.qiniu_tools as qiniu_config
import jishux.settings as settings
from jishux.items import JishuxItem
from jishux.settings import config
from .misc.utils import get_post_type_id


class JishuxPipeline(object):
    def process_item(self, item, spider):
        return item


class JishuxMongoPipeline(object):
    def process_item(self, item, spider):
        return item


class JishuxDataCleaningPipeline(object):
    '''
    数据清洗pipeline
    '''
    def process_item(self, item, spider):
        return item

    def clean_ads(self, item):
        return item

    def clean_tags(self, item):
        return item


# bucket_name = qiniu_config.bucket_name
# image_domain = 'http://7xw8xm.com2.z0.glb.qiniucdn.com/'


class ReplaceImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image_urls']:
            for image_url in item['image_urls']:
                image_url = urljoin(item['post_url'], image_url)
                yield scrapy.Request(image_url)

    # todo 确认是否能不转换gif成静态图
    # def convert_image(self, image, size=None):
    #     buf = BytesIO()
    #     image.save(buf)
    #     return image, buf

    # def image_downloaded(self, response, request, info):
    #     checksum = None
    #     for path, image, buf in self.get_images(response, request, info):
    #         if checksum is None:
    #             buf.seek(0)
    #             checksum = md5sum(buf)
    #         width, height = image.size
    #         self.store.persist_file(
    #             path, buf, info,
    #             meta={'width': width, 'height': height},
    #             headers={'Content-Type': 'image/jpeg'})
    #     return checksum

    def item_completed(self, results, item, info):
        content = item['content_html']
        image_paths = []
        for x in results:
            if x[0]:
                path = self.pre_item(settings.IMAGES_STORE + x[1]['path'])
                image_paths.append(path)
                content = content.replace(x[1]['url'], path)
        if not item['litpic']:
            item['litpic'] = image_paths[0] if len(image_paths) > 0 else ''
        # item['image_paths'] = image_paths
        item['content_html'] = content
        return item

        # 七牛文件上传

    def upload_file(self, file_path, file_name):
        # print(file_path)
        # print(file_name)
        date = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        file_name = 'jishux/' + date + file_name
        q = Auth(qiniu_config.access_key, qiniu_config.secret_key)
        token = q.upload_token(qiniu_config.bucket_name, file_name, 3600)
        ret, info = put_file(token, file_name, file_path)
        assert ret['key'] == file_name
        assert ret['hash'] == etag(file_path)
        # os.remove(file_path)
        return qiniu_config.image_domain + file_name

    # 图片下载上传到七牛,重新拼接img
    def pre_item(self, path):
        return self.upload_file(path, path.split('/')[-1])


class JishuxMysqlPipeline(object):
    def __init__(self):
        # 创建连接git l
        self.connection = pymysql.connect(**config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):

        if isinstance(item, JishuxItem):
            # print(item)
            self.insert_item(item)

    def insert_item(self, item):
        keywords = item['keywords']
        description = item['description']
        content = item['content_html'].replace("'", "\\'") if item['content_html'] else ''
        title = item['post_title'] if item['post_title'] else ''
        source = item['cn_name']
        author = '技术栈' if not item['author'] else item['author']
        litpic = item['litpic'] if item['litpic']else ''
        type_id = get_post_type_id(item['post_type'])
        crawl_time = str(item['crawl_time'])
        sql_insert_meta = 'INSERT INTO dede_archives (typeid, sortrank, flag, ismake, channel, title, writer, source, pubdate, senddate, mid, keywords, description, dutyadmin,voteid,litpic,click) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "'"+%s+"'", "%s", "%s","%s","%s","%s")' % (
            type_id, crawl_time, 'p', -1, 1, title, author, source, crawl_time, crawl_time,
            1, keywords, description, 1, 0, litpic, random.randint(5000, 10000))
        self.cursor.execute(sql_insert_meta)
        sql_last_id = 'SELECT LAST_INSERT_ID()'
        self.cursor.execute(sql_last_id)
        a = self.cursor.fetchone()
        aid = a['LAST_INSERT_ID()']
        sql_insert_content = 'INSERT INTO dede_addonarticle (aid, typeid, body, userip) VALUES(%s,%s,%s,%s)' % (
            aid, type_id, "'" + content + "'", "'" + "127.0.0.1" + "'")
        print(sql_insert_content)
        self.cursor.execute(sql_insert_content)
        sql_insert_arctiny = 'INSERT INTO dede_arctiny (id, typeid, channel, senddate, sortrank,mid) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (
            aid, type_id, 1, crawl_time, crawl_time, 1)
        self.cursor.execute(sql_insert_arctiny)
        for key in keywords.split(','):
            # 判断tag是否在tagindex中存在
            sql_find_tag_exist = "SELECT * FROM dede_tagindex WHERE tag='" + key + "'"
            # 如果不存在插入tag_index '" + key + "'," + type_id + ",1," + crawl_time + "," + crawl_time + "," + crawl_time + "
            sql_insert_tag_index = 'INSERT INTO dede_tagindex (tag, typeid, total, weekup, monthup, addtime) VALUES ("%s",%s,%s,%s,%s,%s)' % (
                key, type_id, 1, crawl_time, crawl_time, crawl_time)
            # print(sql_insert_tag_index)
            # 如果存在则计数+1
            sql_update_count_add_1 = "UPDATE dede_tagindex SET total=total+1  WHERE tag='" + key + "'"
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
            sql_insert_tag_list = "INSERT INTO dede_taglist (tid, aid, arcrank, typeid, tag) VALUES (" + str(
                tid) + "," + str(aid) + ",0," + str(type_id) + ",'" + key + "')"
            print(sql_insert_tag_list)
            self.cursor.execute(sql_insert_tag_list)

        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()
