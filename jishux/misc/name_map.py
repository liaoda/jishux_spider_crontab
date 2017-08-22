#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2017/8/1

from urllib.parse import urlsplit

common_map = {
    # ********** news list ***********
    'http://mobile.51cto.com/': {
        'url': {
            'http://mobile.51cto.com': 'mobile',
        },
        'cn_name': '51CTO',
        'posts_xpath': '//div[@class="home-left-list"]//li',
        'post_url_xpath': 'div[@class="rinfo"]/a/@href',
        'post_title_xpath': 'div[@class="rinfo"]/a/text()',
    },
    'http://socialbeta.com/': {
        'url': {
            'http://socialbeta.com/tag/%E6%A1%88%E4%BE%8B': 'news'
        },
        'cn_name': 'socialbeta',
        'posts_xpath': '//*[@class="postimg"]/li',
        'post_url_xpath': 'div/div/h3/a/@href',
        'post_title_xpath': 'div/div/h3/a/text()',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//*[text()="下一页"]/@href',
        },
    },
    'http://www.qdaily.com/': {
        'url': {
            'http://www.qdaily.com/categories/18.html/': 'news',
            'http://www.qdaily.com/categories/4.html/': 'news',
        },
        'cn_name': '好奇心日报',
        'posts_xpath': '//*[@class="packery-container articles"]/div',
        'post_url_xpath': 'a/@href',
        'post_title_xpath': 'a/div/div/img/@alt',
    },
    'http://www.toodaylab.com/': {
        'url': {
            'http://www.toodaylab.com/field/308': 'news'
        },
        'cn_name': '理想生活实验室',
        'posts_xpath': '//*[@class="content"]/div',
        'post_url_xpath': 'div[@class="post-info"]/p/a/@href',
        'post_title_xpath': 'div[@class="post-info"]/p/a/text()',
    },
    'http://www.madisonboom.com/': {
        'url': {
            'http://www.madisonboom.com/category/works/': 'news'
        },
        'cn_name': '麦迪逊邦',
        'posts_xpath': '//*[@id="gallery_list_elements"]/li',
        'post_url_xpath': 'h3/a/@href',
        'post_title_xpath': 'h3/a/@title',
    },
    'http://iwebad.com/': {
        'url': {
            'http://iwebad.com/': 'news'
        },
        'cn_name': '网络广告人社区',
        'posts_xpath': '//*[@class="new_search_works"]/div',
        'post_url_xpath': 'div[@class="works_info"]/h4/span/a/@href',
        'post_title_xpath': 'div[@class="works_info"]/h4/span/a/text()',
    },
    'http://www.adquan.com/': {
        'url': {
            'http://www.adquan.com/': 'news'
        },
        'cn_name': '广告门',
        'posts_xpath': '//div[@class="w_l_inner"]',
        'post_url_xpath': 'h2/a/@href',
        'post_title_xpath': 'h2/a/text()',
    },
    'http://www.digitaling.com/': {
        'url': {
            'http://www.digitaling.com/projects': 'news'
        },
        'cn_name': '数英网',
        'posts_xpath': '//div[@id="pro_list"]/div',
        'post_url_xpath': 'div[@class="works_bd"]/div/h3/a/@href',
        'post_title_xpath': 'div[@class="works_bd"]/div/h3/a/text()',
    },
    'http://a.iresearch.cn/': {
        'url': {
            'http://a.iresearch.cn/': 'news'
        },
        'cn_name': '艾瑞咨询',
        'posts_xpath': '//div[@id="tab-list"]/div/ul/li',
        'post_url_xpath': 'h3/a/@href',
        'post_title_xpath': 'h3/a/text()',
    },
    'http://www.ebrun.com/': {
        'url': {
            'http://www.ebrun.com/brands/': 'news'
        },
        'cn_name': '亿邦动力网',
        'posts_xpath': '//div[@id="create10"]/div[1]/div[@class="chanlDiv"]',
        'post_url_xpath': 'p/span/a/@href',
        'post_title_xpath': 'p/span/a/text()',
    },
    'https://www.huxiu.com/': {
        'url': {
            'https://www.huxiu.com/': 'news'
        },
        'cn_name': '虎嗅',
        'posts_xpath': '//*[@class="mod-info-flow"]/div[@class="mod-b mod-art "]',
        'post_url_xpath': 'div[@class="mod-thumb "]/a/@href',
        'post_title_xpath': 'div[@class="mod-thumb "]/a/@title',
    },
    'http://api.cyzone.cn/': {
        'url': {
            'http://api.cyzone.cn/index.php?m=content&c=index&a=init&tpl=index_page&page=1': 'news'
        },
        'cn_name': '创业邦',
        'posts_xpath': '//div[@class="article-item clearfix"]',
        'post_url_xpath': 'div[@class="item-intro"]/a/@href',
        'post_title_xpath': 'div[@class="item-intro"]/a/text()',
    },
    'https://www.leiphone.com/': {
        'url': {
            'https://www.leiphone.com/': 'news'
        },
        'cn_name': '雷锋网',
        'posts_xpath': '//*[@class="lph-pageList index-pageList"]/div[2]/ul/li',
        'post_url_xpath': 'div/div[2]/h3/a/@href',
        'post_title_xpath': 'div/div[2]/h3/a/@title',
    },
    'http://www.iheima.com/': {
        'url': {
            'http://www.iheima.com/': 'news'
        },
        'cn_name': 'i黑马',
        'posts_xpath': '//article[@class="item-wrap cf"]',
        'post_url_xpath': 'div/div/a/@href',
        'post_title_xpath': 'div/div/a/text()',
    },
    'http://www.tmtpost.com/': {
        'url': {
            'http://www.tmtpost.com/': 'news'
        },
        'cn_name': '钛媒体',
        'posts_xpath': '//li[@class="post_part clear"]',
        'post_url_xpath': 'div/h3/a/@href',
        'post_title_xpath': 'div/h3/a/text()',
    },
    'http://www.iyiou.com/': {
        'url': {
            'http://www.iyiou.com/newpost': 'news'
        },
        'cn_name': '亿欧网',
        'posts_xpath': '//ul[@class="specificpost-list"]/li[@class="clearFix"]',
        'post_url_xpath': 'div/a/@href',
        'post_title_xpath': 'div/a/@title',
    },
    'http://www.im2maker.com/': {
        'url': {
            'http://www.im2maker.com/fresh/': 'news'
        },
        'cn_name': '镁客网',
        'posts_xpath': '//div[@id="article-list"]/div',
        'post_url_xpath': 'div/a[2]/@href',
        'post_title_xpath': 'div/a[2]/@title',
    },
    'http://www.geekpark.net/': {
        'url': {
            'http://www.geekpark.net/': 'news'
        },
        'cn_name': '极客公园',
        'posts_xpath': '//*[@id="collection-all"]/div/article[@class="article-item"]',
        'post_url_xpath': 'div/div/a[2]/@href',
        'post_title_xpath': 'div/div/a[2]/text()',
    },
    'http://www.ikanchai.com/': {
        'url': {
            'http://www.ikanchai.com/': 'news'
        },
        'cn_name': '砍柴网',
        'posts_xpath': '//*[@id="mainList"]/ul/li[@class="rtmj-box"]',
        'post_url_xpath': 'dl/dt/a/@href',
        'post_title_xpath': 'dl/dt/a/@title',
    },
    'http://www.lieyunwang.com/': {
        'url': {
            'http://www.lieyunwang.com/': 'news'
        },
        'cn_name': '猎云网',
        'posts_xpath': '//*[@class="article-bar clearfix"]',
        'post_url_xpath': 'div/a/@href',
        'post_title_xpath': 'div/a/text()',
    },
    'https://www.jiqizhixin.com/': {
        'url': {
            'https://www.jiqizhixin.com/': 'news'
        },
        'cn_name': '机器之心',
        'posts_xpath': '//*[@class="article-inline"]',
        'post_url_xpath': 'div/a/@href',
        'post_title_xpath': 'div/a/@title',
    },
    'http://www.donews.com/': {
        'url': {
            'http://www.donews.com/': 'news'
        },
        'cn_name': 'donews',
        'posts_xpath': '//dl[@class="block pb30 mb30 line_b clearfix"]',
        'post_url_xpath': 'dd/h3/a/@href',
        'post_title_xpath': 'dd/h3/a/text()',
    },
    'http://news.chinabyte.com/': {
        'url': {
            'http://news.chinabyte.com/': 'news'
        },
        'cn_name': '比特网',
        'posts_xpath': '//div[@class="sec_left"]/div[2]/div[not(contains(@class, "Browse_more"))]',
        'post_url_xpath': 'div[@class="hot_"]/h4/a/@href',
        'post_title_xpath': 'div[@class="hot_"]/h4/a/text()',
    },
    'http://www.sootoo.com/': {
        'url': {
            'http://www.sootoo.com/tag/1/?&day=--&page=1': 'news'
        },
        'cn_name': '速途网',
        'posts_xpath': '//li[@class="ZXGX_list clearfix"]',
        'post_url_xpath': 'h3/a/@href',
        'post_title_xpath': 'h3/a/text()',
    },
    'http://www.jiemian.com/': {
        'url': {
            'http://www.jiemian.com/lists/49.html': 'news',
            'http://www.jiemian.com/lists/6.html': 'news',
            'http://www.jiemian.com/lists/66.html': 'news',
            'http://www.jiemian.com/lists/73.html': 'news',
        },
        'cn_name': '界面',
        'posts_xpath': '//div[@id="load-list"]/div',
        'post_url_xpath': 'div/a/@href',
        'post_title_xpath': 'div/a/@title',
        'post_type': 'news',
    },
    'http://cn.technode.com/': {
        'url': {
            'http://cn.technode.com/post/category/technode-talks/': 'news',
        },
        'cn_name': '动点科技',
        'posts_xpath': '//div[@class="td_mod_wrap td_mod9 "]',
        'post_url_xpath': 'div/a/@href',
        'post_title_xpath': 'div/a/@title',
    },
    'http://www.2cto.com/': {
        'url': {
            'http://www.2cto.com/article/web/': 'frontend',
            'http://www.2cto.com/kf/yidong/Android/news/': 'mobile',
            'http://www.2cto.com/ebook/jiaoben/Python/': 'backend',
            'http://www.2cto.com/ebook/safe/': 'network',
        },
        'cn_name': '红黑联盟',
        'posts_xpath': '//*[@id="fontzoom"]/ul/li',
        'post_url_xpath': 'a/@href',
        'post_title_xpath': 'a/text()',
    },


    # '': {
    #     'url': '',
    #     'cn_name': '',
    #     'posts_xpath': '',
    #     'post_url_xpath': '',
    #     'post_title_xpath': '',
    #     'post_type': '',
    #     'next_page': {
    #         'type': '',
    #         'xpath': '',
    #     },
    #     'headers': {
    #         'key1': 'value',
    #         'key2': 'value',
    #         'key3': 'value',
    #         'key4': 'value',
    #     },
    # },

    # '': {
    #     # [必选] url: 起始抓取地址
    #     'url': '',
    #     # [必选] cn_name: 中文名称，用于显示转载网站
    #     'cn_name': '',
    #     # [必选] posts_xpath: 文章列表xpath
    #     'posts_xpath': '',
    #     # [必选] post_url_xpath: 列表单个item的超链接xpath
    #     'post_url_xpath': '',
    #     # [必选] post_title_xpath: 列表单个item的标题xpath
    #     'post_title_xpath': '',
    #     # [必选] post_type: 文章类型，比如news,bigdata,mobile
    #     'post_type': '',
    #     # [可选] next_page: 下一页具体配置
    #     'next_page': {
    #         'type': '',
    #         'xpath': '',
    #     },
    #     # [可选] headers: 请求所需特殊headers，例如Referer
    #     'headers': {
    #         'key1': 'value',
    #         'key2': 'value',
    #         'key3': 'value',
    #         'key4': 'value',
    #     },
    # },

}


def get_start_urls():
    start_urls = []
    for k in common_map.keys():
        start_urls += common_map[k]['url'].keys()
    return start_urls


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
