#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/9
import time, re, datetime
from dateutil import parser

def time_format(time_stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(time_stamp)))


time_re = re.compile('[年月日\s]')


def generate_timestamp(post_time):

    min = re.search('(\d{1,2}(?=\s?分钟前))', post_time)
    if min:
        return int((datetime.datetime.now() - datetime.timedelta(minutes=int(min.group()))).timestamp())

    hour = re.search('(\d{1,2}(?=\s?小时前))', post_time)
    if hour:
        return int((datetime.datetime.now() - datetime.timedelta(hours=int(hour.group()))).timestamp())
    day = re.search('(\d{1,2}(?=\s?天前))', post_time)
    if day:
        return int((datetime.datetime.now() - datetime.timedelta(days=int(day.group()))).timestamp())
        # parser.parse(time_re.sub(' ', '2015 年 5 月 4 日 12:30:23'))
    # for i in re_map.keys():
    #     if re.search(i, post_time):
    #         return int(time.mktime(time.strptime(post_time, re_map[i])))
    try:
        return int(parser.parse(time_re.sub(' ', post_time)).timestamp())
    except:
        return None

#
regu = re.compile('(\d{4}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s\d{2}:\d{2}(:\d{2})?)?)|(\d{1,2}(?=\s?(分钟|小时|天)前))')
#






