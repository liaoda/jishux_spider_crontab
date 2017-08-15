#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/13

import jieba.analyse

def get_description(response, content_text):
    description = response.xpath('//meta[@name="description"]/@content')
    if description:
        description = description.extract_first()
    elif len(description) >= 100:
        description = content_text[0:100]
    else:
        description = content_text
    return description


def get_keywords(response, content_text):
    keywords = response.xpath('//meta[@name="keywords"]/@content')
    if keywords:
        keywords = keywords.extract_first()
    else:
        keywords = jieba.analyse.extract_tags(str, topK=3)
        keywords = ','.join(keywords)
    return keywords