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


# str = '''
# <div><div id="content">&#13;   &#13;<p><img class="alignCenter" title="我理解的大数据（二）的图片" src="..http://7xw8xm.com2.z0.glb.qiniucdn.com/jishux/2017/08/243eefcf8d7128449e8a7df666c8300ff087b910ad.jpg?imageMogr2/interlace/1" alt=""/></p>&#13;<p>      昨天偷懒了少了一次文字排版，没想到好多朋友发消息来说字体变小了不习惯，看来坚持大一点的字体还是有好处的。</p>&#13;<p>      虽然很想保持高频率更新，但没想到回阿里后工作竟然比创业时还忙。经常回家得比较晚，再加上每天脑力使用过度，所以竟是硬生生的断更了两周。在接下来我想如果可能的话，把更新的时间调整到周日的晚上，周末可能会稍微空闲点。</p>&#13;<p>      在此也再征集一下大家想看的话题，可以向我提问，我会选取部分作为接下来文章的选题。</p>&#13;<p>      延伸一下昨天关于<a rel="nofollow" href="http://www.thebigdata.cn/YeJieDongTai/7180.html" target="_blank" title="">大数据</a>的话题。在安全行业里未来真正会具备核心竞争力的，我认为正是这样的全局视角带来的改变。</p>&#13;<p>      比如近年来兴起的「撞库」攻击。因为各大公司用户数据的泄露，黑客手上已经拥有了数十亿条用户数据，其中20%包含了明文密码。在过去黑客想破解 一个用户的密码，可能会通过字符的排列组合生成一部字典，逐个尝试，这样破解的效率无疑是相当低的。但现在因为有了全网用户的「密码库」，只需要简单的查 询用户名，多半就能知道密码是什么，简单粗暴。</p>&#13;<p>      大数据就应该这么简单粗暴的应用，以一种完全不讲道理的方式直接达到效果，根本不需要什么精巧的算法，就像「把大象装进冰箱」里一样。</p>&#13;<p>      类似的，国外一家安全公司Akamai宣称他们能非常有效的阻断DDoS攻击，原因是他们通过和运营商合作的方式获取了全球30%左右的流量，从而能有效的监控到全球所有的恶意IP，发现有攻击过来，直接根据IP信息就阻断了。这也是大数据的一种典型应用。</p>&#13;<p>      再举一个例子，数据可能来自于过去没有注意到的地方。对于电话诈骗的传统解决思路，一般是从用户的来电号码着手，或者是从周边信息比如短信、传播 来源入手。这些传统方法已经逐渐的变得效率低下。但目前有一种解决思路是根据用户的「声纹」信息进行有效识别，这样只要积累了一个用户的「声纹信息库」， 就能够在每个用户通话时，直接识别出被标记为诈骗的那个用户。</p>&#13;<p>      所谓「声纹」就像是指纹信息一样，每个人说话的声音其实都是独一无二的，通过数字化的方法能够有效的识别出来。目前国外一些安全公司会把这种技术 用在Call Center中进行反欺诈。但声纹信息和指纹信息一样，会成为国家安全基础设施的一部分。比如国外的一些机构，一旦掌握了所有中国人，包括政府领导人的指 纹信息，会酿成什么后果很难想象。这也是为什么中国政府的工作人员会禁用苹果手机的原因，至少苹果收集用户的指纹信息会威胁到国家安全。</p>&#13;<p>      所以，我理解的大数据，和各种复杂的算法没有直接关系，那最多只是锦上添花。我理解的大数据，就是这么简单粗暴，以高一个维度的视角毫不讲道理的直捣黄龙。</p>&#13;<p>      两点之间什么最短？在二维空间是直线最短。但到了三维空间，两点之间距离可以为零（虫洞），比如把一张纸上的两点对折后贴起来。</p>&#13;<img src="../..http://7xw8xm.com2.z0.glb.qiniucdn.com/jishux/2017/08/24a9a7927c38b554cc3a3e6ed36472a843ab197411.jpg?imageMogr2/interlace/1" alt=""/>&#13;</div>&#13;&#13;&#13;&#13;</div>
#
# '''
#
# reee = re.compile('src=".*?'+'http://7xw8xm.com2.z0.glb.qiniucdn.com/jishux/2017/08/243eefcf8d7128449e8a7df666c8300ff087b910ad.jpg?imageMogr2/interlace/1')
#
#
# print(reee.sub('src="what the fuck', str))