# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jishux.items import JishuxItem
from scrapy.exceptions import DropItem
import pymysql
from jishux.settings import config


class JishuxPipeline(object):
    def process_item(self, item, spider):
        return item


class JishuxMongoPipeline(object):
    def process_item(self, item, spider):
        return item


# class JishuxMysqlPipeline(object):
#     def __init__(self):
#         self.connection = pymysql.connect(host='47.93.232.8', port=3306, user='root', passwd='a8JcZ79XW3Krdbtj',
#                                           db='dedecmsv57utf8sp2', charset='utf8')
#         self.cursor = self.connection.cursor()
#
#     def process_item(self, item, spider):
#         # dedecms sql
#         source = u'技术栈'
#         keywords = item['keywords']
#         description = item['description']
#         sql = 'INSERT INTO dede_archives (typeid, sortrank, flag, ismake, channel, title, writer, source, pubdate, senddate, mid, keywords, description, dutyadmin) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
#             2, item['crawl_time'], 'p', -1, 1, item['post_title'], 'admin', source, item['crawl_time'],
#             item['crawl_time'], 1, keywords, description, 1
#         )
#         # print [sql], '********'
#         self.cursor.execute(sql)
#         sql2 = 'SELECT LAST_INSERT_ID()'
#         self.cursor.execute(sql2)
#         a = self.cursor.fetchone()
#         aid = a[0]
#         sql3 = 'INSERT INTO dede_addonarticle (aid, typeid, body, userip) VALUES ("%s", "%s", "%s", "%s")' % (
#             aid, 2, item['content_html'].replace(r'"', r'\"'), '127.0.0.1')
#         self.cursor.execute(sql3)
#         # print [sql3], '********'
#         sql4 = 'INSERT INTO dede_arctiny (id, typeid, channel, senddate, sortrank) VALUES ("%s", "%s", "%s", "%s", "%s")' % (
#             aid, 2, 1, item['crawl_time'], item['crawl_time'])
#         self.cursor.execute(sql4)
#         # print [sql4], '********'
#         self.connection.commit()
#         return item
#
#     def close_spider(self, spider):
#         self.connection.close()
#
#



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
        print(keywords)
        description = item['description']
        content = item['content_html'].replace("'", "\\'") if item['content_html'] else ''
        title = item['post_title'] if item['post_title'] else ''
        source = '技术栈'
        author = '' if not item['author'] else item['author']
        litpic = item['litpic'] if item['litpic']else ''
        type_id = item['type_id'] if item['type_id'] else 2
        sql_insert_meta = 'INSERT INTO dede_archives (typeid, sortrank, flag, ismake, channel, title, writer, source, pubdate, senddate, mid, keywords, description, dutyadmin,voteid,litpic,source) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "'"+%s+"'", "%s", "%s","%s","%s","%s")' % (
            type_id, item['crawl_time'], 'p', -1, 1, title, 'admin', author, item['crawl_time'], item['crawl_time'],
            1, keywords, description, 1, 0, litpic, source)
        self.cursor.execute(sql_insert_meta)
        sql_last_id = 'SELECT LAST_INSERT_ID()'
        self.cursor.execute(sql_last_id)
        a = self.cursor.fetchone()
        aid = a['LAST_INSERT_ID()']
        sql_insert_content = "INSERT INTO dede_addonarticle (aid, typeid, body, userip) VALUES (" + str(
            aid) + "," + str(
            type_id) + "," + "'" + content + "'" + ",'127.0.0.1')"
        # print(sql_insert_content)
        self.cursor.execute(sql_insert_content)
        sql_insert_arctiny = 'INSERT INTO dede_arctiny (id, typeid, channel, senddate, sortrank,mid) VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (
            aid, type_id, 1, item['crawl_time'], item['crawl_time'], 1)
        self.cursor.execute(sql_insert_arctiny)
        for key in keywords.split(','):
            # 判断tag是否在tagindex中存在
            sql_find_tag_exist = "SELECT * FROM dede_tagindex WHERE tag='" + key + "'"
            # 如果不存在插入tag_index
            sql_insert_tag_index = "INSERT INTO dede_tagindex (tag, typeid, total, weekup, monthup, addtime) VALUES ('" + key + "'," + str(
                type_id) + ",1," + item['crawl_time'] + "," + item['crawl_time'] + "," + item['crawl_time'] + ")"
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
