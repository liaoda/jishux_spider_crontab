#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/29
import re
from urllib.parse import urlsplit


def clean_tags(item):
    '''
    加工标签
    '''
    content_html = item['content_html']
    # nofollow
    content_html = content_html.replace('<a', '<a rel="nofollow"')
    # 空白符的处理
    content_html = content_html.strip().replace('\r', '').replace('\n', '').replace('\t', '')
    p1 = re.compile('<p>(\s*|<br>|<br/>|&nbsp;)</p>')
    content_html = re.sub(p1, '', content_html)
    # 去掉标签和标签之间多余的空白符号
    p2 = re.compile('>\s+<')
    content_html = re.sub(p2, '><', content_html)
    # TODO: 代码标签统一处理
    # 把img标签里面的懒加载的data-src，换成src
    content_html = content_html.replace('data-src=', 'src=')
    # 赋值
    item['content_html'] = content_html
    return item


def clean_ads(item):
    '''
    清洗广告
    '''
    # TODO 清洗广告
    return item
