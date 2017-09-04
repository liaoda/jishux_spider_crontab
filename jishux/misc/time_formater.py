#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/9
import re
import dateparser
import time
import random

time_re = re.compile('[年月日\s]')


def generate_timestamp(post_time):
    now = int(time.time())
    date_time = dateparser.parse(time_re.sub(' ', post_time))
    if date_time:
        time_stamp = int(date_time.timestamp())
    else:
        return now
    if time_stamp > now:
        time_stamp = now - random.randint(0, 600)
    return time_stamp


# param = {
#     'page': 1,
#     'order_by':'added_at'
# }
# url = 'http://www.jianshu.com/c/V2CqjW?order_by=added_at&page={page}'
#
# for i in param.keys():
#     url = url.replace('{' + i + '}', str(param[i]))
#
# print(url)
#
# for i in range(10):
#     for key in param.keys():
#         reg1 = '(?={0}=).*?&?'.format(key)
#         print(reg1)
#         s = re.search(reg1, url)
#         print(s)
