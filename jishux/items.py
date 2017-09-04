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
    post_type = scrapy.Field()  # 类型id
    post_url = scrapy.Field()  # 文章url
    post_title = scrapy.Field()  # 文章名
    _id = scrapy.Field()  # ..
    cn_name = scrapy.Field()  # 站点名
    image_urls = scrapy.Field()  # 文章中的图片链接
    domain = scrapy.Field()  # 网站域名 图片地址为相对路径时使用
    qiniu_urls=scrapy.Field() #上传之后的七牛url