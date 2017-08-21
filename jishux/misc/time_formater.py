#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/9
import re
import dateparser
time_re = re.compile('[年月日\s]')


def generate_timestamp(post_time):
    return int(dateparser.parse(time_re.sub(' ', post_time)).timestamp())
