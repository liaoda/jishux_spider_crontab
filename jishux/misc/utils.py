#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/17

def get_post_type_id(post_type):
    if not post_type:
        return None

    type_map = {
        'news': 2,
        'bigdata': 5,
        'mobile': 24,
        'ai': 10,
        'database': 11,
        'other': 12,
        'network': 13,
        'system': 14,
        'frontend': 19,
        'backend': 20,
    }
    return type_map[post_type]
