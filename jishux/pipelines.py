# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import urllib
from misc.time_formater import time_format


class JishuxPipeline(object):
    def process_item(self, item, spider):
        return item


class JishuxMongoPipeline(object):
    def process_item(self, item, spider):
        return item


class JishuxMysqlPipeline(object):
    def __init__(self):
        self.connection = MySQLdb.connect(host='47.93.232.8', port=3306, user='root', passwd='a8JcZ79XW3Krdbtj',
                                          db='dedecmsv57utf8sp2', charset='utf8')
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        time_f = time_format(item['crawl_time'])
        # wordpress sql
        # sql = 'insert into wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_status, comment_status, ping_status, post_name, post_modified, post_modified_gmt, post_parent, menu_order, post_type, comment_count) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s")' % (
        #     '1', time_f, time_f, item['content_html'].replace(r'"', r'\"'), item['post_title'], 'publish', 'open', 'open', urllib.quote(item['post_title'].encode('utf-8')), time_f, time_f, '0', '0', 'post', '0')

        # dedecms sql
        source = u'技术栈'
        keywords = item['keywords']
        description = item['description']
        sql = 'INSERT INTO dede_archives (typeid, sortrank, flag, ismake, channel, title, writer, source, pubdate, senddate, mid, keywords, description, dutyadmin) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
            2, item['crawl_time'], 'p', -1, 1, item['post_title'], 'admin', source, item['crawl_time'], item['crawl_time'], 1, keywords, description, 1
        )
        print [sql], '********'
        self.cursor.execute(sql)
        sql2 = 'SELECT LAST_INSERT_ID()'
        self.cursor.execute(sql2)
        a = self.cursor.fetchone()
        aid = a[0]
        sql3 = 'INSERT INTO dede_addonarticle (aid, typeid, body, userip) VALUES ("%s", "%s", "%s", "%s")' % (aid, 2, item['content_html'].replace(r'"', r'\"'), '127.0.0.1')
        self.cursor.execute(sql3)
        print [sql3], '********'
        sql4 = 'INSERT INTO dede_arctiny (id, typeid, channel, senddate, sortrank) VALUES ("%s", "%s", "%s", "%s", "%s")' % (aid, 2, 1, item['crawl_time'], item['crawl_time'])
        self.cursor.execute(sql4)
        print [sql4], '********'
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()