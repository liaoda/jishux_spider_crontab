#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/9
import time
def time_format(time_stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(time_stamp)))