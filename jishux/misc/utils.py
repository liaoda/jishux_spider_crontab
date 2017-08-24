#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/17

import hashlib


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
