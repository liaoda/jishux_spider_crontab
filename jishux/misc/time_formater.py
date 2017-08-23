#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/9
import re
import dateparser
time_re = re.compile('[年月日\s]')


def generate_timestamp(post_time):
    return int(dateparser.parse(time_re.sub(' ', post_time)).timestamp())





# recode = re.compile('(<pre\s?.*?>)\s*?(<code>)*')
# recode2 = re.compile('(</code>)*\s*</pre>')
#
#
# s =  recode.sub('<pre><code>', str)
# print(type(s))
# s =  recode2.sub('</code></pre>', s)
# print(s)