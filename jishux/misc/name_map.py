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
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//*[text()="下一页"]/@href',
        },
        'cn_name': '红黑联盟',
        'posts_xpath': '//*[@id="fontzoom"]/ul/li',
        'post_url_xpath': 'a/@href',
        'post_title_xpath': 'a/text()',
    },

    'http://www.xitongcheng.com/': {
        'url': {
            'http://www.xitongcheng.com/jiaocheng/xtazjc/': 'os',
            'http://www.xitongcheng.com/jiaocheng/xp/': 'os',
            'http://www.xitongcheng.com/jiaocheng/win7/': 'os',
            'http://www.xitongcheng.com/jiaocheng/win8/': 'os',
            'http://www.xitongcheng.com/jiaocheng/win10/': 'os',
            'http://www.xitongcheng.com/jiaocheng/dnrj/': 'os',
        },
        'cn_name': '系统城',
        'posts_xpath': '//div[@class="left"]/ul/li',
        'post_url_xpath': 'a/@href',
        'post_title_xpath': 'a/text()',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//*[text()="下一页"]/@href',
        },
    },

    'http://www.linuxidc.com/': {
        'url': {
            'http://www.linuxidc.com/it/': 'news',
            'http://www.linuxidc.com/Linuxit/': 'os',
            'http://www.linuxidc.com/linuxsoft/': 'os',
            'http://www.linuxidc.com/MySql/': 'db',
            'http://www.linuxidc.com/RedLinux/': 'other',
            'http://www.linuxidc.com/download/': 'other',
            'http://www.linuxidc.com/Apache/': 'network',
            'http://www.linuxidc.com/Unix/': 'network',
        },
        'cn_name': 'linux公社',
        'posts_xpath': '//div[@class="summary"]',
        'post_url_xpath': 'div[@class="cont"]/div[@class="title"]/a/@href',
        'post_title_xpath': 'div[@class="cont"]/div[@class="title"]/a/text()',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//*[text()="»"]/@href',
        },
    },

    'https://linux.cn/': {
        'url': {
            'https://linux.cn/news/': 'news',
            'https://linux.cn/tech/': 'os',
            'https://linux.cn/talk/': 'os',
            'https://linux.cn/share/': 'os',
        },
        'cn_name': 'Linux中国',
        'posts_xpath': '//ul[@class="article-list leftpic"]',
        'post_url_xpath': 'li/h2/span[@class="title"]/a/@href',
        'post_title_xpath': 'li/h2/span[@class="title"]/a/@title',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//a[text()="下一页"]',
        },
    },

    'http://www.thebigdata.cn/': {
        'url': {
            'http://www.thebigdata.cn/YeJieDongTai/': 'news',
            'http://www.thebigdata.cn/KaiYuanJiShu/': 'bigdata',
            'http://www.thebigdata.cn/YingYongAnLi/': 'bigdata',
            'http://www.thebigdata.cn/JieJueFangAn/': 'bigdata',
            'http://www.thebigdata.cn/ShangYePingTai/': 'bigdata',
            'http://www.thebigdata.cn/ShuJuFenXi/': 'bigdata',
        },
        'cn_name': '中国大数据',
        'posts_xpath': '//div[@class="summary"]',
        'post_url_xpath': 'div[@class="cont"]/div[@class="title"]/a/@href',
        'post_title_xpath': 'div[@class="cont"]/div[@class="title"]/a/text()',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//*[text()="»"]/@href',
        },
    },

    'http://it.dataguru.cn/': {
        'url': {
            'http://it.dataguru.cn/': 'bigdata',
        },
        'cn_name': '炼数成金',
        'posts_xpath': '//dl[@class="bbda cl"]',
        'post_url_xpath': 'dt/a/@href',
        'post_title_xpath': 'dt/a/text()',
        'next_page': {
            'type': 'CLICK_NEXT_BUTTON',
            'xpath': '//a[text()="下一页"]',
        },
    },

    'http://www.jianshu.com/': {
        'url': {
            'http://www.jianshu.com/c/V2CqjW': 'bigdata',
            'http://www.jianshu.com/c/c261fa3879d6': 'frontend',
            'http://www.jianshu.com/c/0bab91ded569': 'other',
            'http://www.jianshu.com/c/51425dc50685': 'os',
            'http://www.jianshu.com/c/5aac963ca52d': 'mobile',
            'http://www.jianshu.com/c/b641f7c33fd2': 'bigdata',
            'http://www.jianshu.com/c/257bcc1383e2': 'ai',
            'http://www.jianshu.com/c/1395428608b4': 'ai',
            'http://www.jianshu.com/c/1022d2287ccc': 'ai',
            'http://www.jianshu.com/c/f971e98846c6': 'network',
        },
        'cn_name': '简书',
        'posts_xpath': '//*[contains(@id,"note")]',
        'post_url_xpath': 'div/a[@class="title"]/@href',
        'post_title_xpath': 'div/a[@class="title"]/text()',
        'headers': {
            "Accept-Encoding": "gzip, identity",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cookie": "remember_user_token=W1syMjEwMDk4XSwiJDJhJDEwJDZQU3ZteVdlMjkvdjdVVURDNjB0OWUiLCIxNTAzNDgyNjMwLjkyNDIxMTciXQ==--32ae8134ca911d1d332f8f8c42998581b18eb5ea; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1502267438,1502849321,1503026189,1503482168; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1503483324; _ga=GA1.2.938018437.1493976814; _gid=GA1.2.392185505.1503482168; _session_id=dGVjRndIQkNNYUx3UVN5YnFIMnlHd0pRSG9aR05XVS9pYnNTbU5kVExWSzVJelBxT2RSeUFqOEJjeFMzSDNTVU40aHpMbjQzWmpNQkFLRFdIWHZBcmxPZEc5aFdGaWYwdXVpSkVFL0tpbmlJdU1udzVUbU1uZnhMR0crYnR6RktEMmdIQkpyOXM1N3RyS1MwcEt4YnJybUg1bktYTHo1SStlN0U3Yk1vektTUzdhOXVtOVRJakxTa2xLTHRtcmVkdFBNQUZiay9QRWVzQlRKblk1Q0ZjL2VrckZQNHJ2QmxFOXMvaEw3T1BZUUcwYURsQjF2anBaN1JlSldBeXhtbCtjc2grYVpqOCtFOEpjRlAySlpxNHBQc0NhZjhicjVGcFBKOWRLdEdYZndabUtOTXNvdktsT3l1V1g1aC9GNms2VzhkZVJ3QXdNRS82cjhiSU52ZWdkSkFKNUd0dnpRUFJvYzAzVXl1alBNalArVGM3bWVkd0lQYXhYS1A5N1ZiYXF5eWZkLzhoR2prekxoOHRUUmE1dlNDK2lwMkFnb0dtMHBEc242Wm1pQT0tLWsxc2UvUDlhWnR5Qk1aQkJ3TWxsTmc9PQ==--0bfa89637e8adbc729937a3a07b21cf7c76723aa",
            "If-None-Match": "W/\"baebc4bb3d3c66947d8cbdedf66a8726\"",
        }
    },

    # '': {
    #     'url': {
    #         '': '',
    #     },
    #     'cn_name': '',
    #     'posts_xpath': '',
    #     'post_url_xpath': '',
    #     'post_title_xpath': '',
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


def get_all_site_start_urls():
    start_urls = []
    for k in common_map.keys():
        start_urls += common_map[k]['url'].keys()
    return start_urls


def get_one_site_start_urls(host=''):
    return common_map[host]['url'].keys()


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

