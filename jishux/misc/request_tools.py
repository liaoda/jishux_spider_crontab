#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/7

from scrapy import Request


# 翻页
def next_page(callback, response, conf, first_url, latest_url, post_type):
    if 'next_page' in conf.keys():
        next_page_type = conf['next_page']['type']
    else:
        return None

    # function list
    def click_next_button():
        next_page_xpath = conf['next_page']['xpath']
        next_url = response.xpath(next_page_xpath)
        if next_url == response.url:
            return None
        if next_url:
            next_url = response.urljoin(next_url.extract_first())
            request = Request(url=next_url, callback=callback,
                              headers=conf['headers'] if 'headers' in conf.keys() else None)
            request.meta['first_url'] = first_url
            request.meta['latest_url'] = latest_url
            request.meta['conf'] = conf
            request.meta['post_type'] = post_type
            request.meta['request_url'] = next_url
            return request

    # fuction map
    func_map = {
        'CLICK_NEXT_BUTTON': click_next_button,
    }

    # execute function
    return func_map[next_page_type]()
