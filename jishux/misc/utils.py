#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/17

import hashlib
from urllib.parse import urlsplit

from .all_secret_set import start_urls_config
from .name_map import common_map


def get_post_type_id(post_type):
    if not post_type:
        return 2

    type_map = {
        'news': 2,
        'bigdata': 5,
        'mobile': 24,
        'ai': 10,
        'db': 11,
        'other': 12,
        'network': 13,
        'os': 14,
        'frontend': 19,
        'backend': 20,
    }
    return type_map[post_type] if post_type in type_map.keys() else 2


def md5(s):
    m5 = hashlib.md5()
    m5.update(s.encode('utf8'))
    return m5.hexdigest()


def get_all_site_start_urls():
    start_urls = []
    for k in common_map.keys():
        start_urls += common_map[k]['url'].keys()
    return start_urls


def get_one_site_start_urls(host=[]):
    first_url = host[0] if host else ''
    if first_url in common_map.keys() or first_url[0:-1] in common_map.keys():
        return list(common_map[first_url]['url'].keys())
    else:
        return host


def get_start_urls():
    all = start_urls_config['all']
    one = start_urls_config['start_urls']

    if all:
        return get_all_site_start_urls()
    else:
        return get_one_site_start_urls(host=one)


def get_conf(url):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    conf = None
    if url in common_map.keys():
        conf = common_map[url]
    elif base_url in common_map.keys():
        conf = common_map[base_url]
    elif base_url[0:-1] in common_map.keys():
        conf = common_map[base_url]
    return conf


def get_cookies(str_cookie):
    if str_cookie is None:
        return None
    cookie = {}
    arr = str_cookie.split(';')
    for i in arr:
        arrs = i.split('=', 1)
        cookie[arrs[0]] = arrs[1]

    return cookie
