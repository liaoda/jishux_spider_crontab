# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JishuxItem(scrapy.Item):
    content_html = scrapy.Field()  # 内容 html
    keywords = scrapy.Field()  # tag
    author = scrapy.Field()  # 作者
    crawl_time = scrapy.Field()  # 时间
    description = scrapy.Field()  # 描述
    litpic = scrapy.Field()  # 缩略图
    type_id = scrapy.Field()  # 类型id
    post_url = scrapy.Field()  # 文章url
    post_title = scrapy.Field()  # 文章名
    post_id = scrapy.Field()  # ..
    site_name = scrapy.Field()  # 站点名
