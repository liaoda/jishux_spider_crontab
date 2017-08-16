#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/7

import time

import scrapy
from scrapy import Selector

from ..items import JishuxItem
from ..misc.name_map import common_map
from ..misc.readability_tools import get_summary
from ..misc.request_tools import next_page
from ..misc.text_tools import get_description, get_keywords
from ..misc.sqlite_tools import get_then_change_latest_url


class CommonSpider(scrapy.Spider):
    name = 'common_spider'
    # 爬所有的网站
    # start_urls = common_map.keys()
    # 爬单个网站
    start_urls = ['http://socialbeta.com/tag/%E6%A1%88%E4%BE%8B']
    custom_settings = {
        'ITEM_PIPELINES': {
            'jishux.pipelines.JishuxMysqlPipeline': 300,
        },
        'SPIDER_MIDDLEWARES': {
            'jishux.middlewares.JishuxSpiderMiddleware': 543,
        }
    }

    def parse(self, response):
        # 本次最新的文章的url
        first_url = response.meta['first_url'] if 'first_url' in response.meta.keys() else None
        # 上一次的最新的文章的url
        latest_url = response.meta['latest_url'] if 'latest_url' in response.meta.keys() else None
        conf = response.meta['conf'] if 'conf' in response.meta.keys() else common_map[response.url]

        posts = response.xpath(conf['posts_xpath'])
        for post in posts:
            post_url = post.xpath(conf['post_url_xpath']).extract_first()
            post_url = response.urljoin(post_url)
            post_title = post.xpath(conf['post_title_xpath']).extract_first()
            post_title = post_title.strip().replace('\r', '').replace('\n', '').replace('\t', '')
            item = {
                '_id': post_url,
                'post_url': post_url,
                'post_title': post_title
            }

            # 把第一条数据作为最新的数据，存储到sqlite中
            if not first_url:
                first_url = post_url
                latest_url = get_then_change_latest_url(conf['name'], first_url)
            # 从sqlite中取出上一次最新的数据，与本次的数据做对比，如果相同则认为文章抓到了上次已经抓过的数据，如果不同则认为文章还没有抓完
            if post_url == latest_url:
                print(u'{} - 爬到了上次爬到的地方'.format(conf['cn_name']))
                return

            request = scrapy.Request(url=post_url, callback=self.parse_post,
                                     headers=conf['headers'] if 'headers' in conf.keys() else None)
            request.meta['item'] = item
            request.meta['conf'] = conf
            print(post_title)
            yield request

        # 翻页
        request = next_page(callback=self.parse, response=response, conf=conf, first_url=first_url,
                            latest_url=latest_url)
        if request:
            yield request

    def parse_post(self, response):
        item = JishuxItem()
        item['post_url'] = response.meta['item']['post_url']
        item['post_title'] = response.meta['item']['post_title']
        item['_id'] = response.meta['item']['_id']
        conf = response.meta['conf']
        content_html = get_summary(response.text)
        content_text = Selector(text=content_html).xpath('string(.)').extract_first()
        content_text = content_text.strip().replace('\r', '').replace('\n', '').replace('\t', '')
        description = get_description(response, content_text)
        keywords = get_keywords(response, content_text)
        # item['content_text'] = content_text
        item['litpic'] = ''  # todo 文章缩略图
        item['content_html'] = content_html
        item['description'] = description
        item['keywords'] = keywords
        item['crawl_time'] = int(time.time())
        item['site_name'] = conf['cn_name']
        item['author'] = ''  # todo 文章作者 配置文件需要适配
        item['type_id'] = conf['type_id']  # todo 文章类型需要和配置文件里id适配
        item['image_urls'] = Selector(text=content_html).xpath('//img/@src').extract()  # todo 获得网页内容中的图片链接,需要从内容中筛选
        yield item
