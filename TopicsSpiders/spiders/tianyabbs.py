# -*- coding: utf-8 -*-
"""
天涯论坛
"""
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TianyabbsSpider(CrawlSpider):
    """
    增加栏目的时候仅需将URL上栏目的特征码填入下面的字典即可
    """
    name = 'tianyabbs'
    allowed_domains = ['bbs.tianya.cn']
    start_urls = ['http://bbs.tianya.cn/', ]

    url_keywords = {
        'feeling': '情感天地',
        '98': '亲子中心',
        '14': '开心乐园',
        '1095': '生活那些事',
        '934': '婆媳关系',
        'no05': '煮酒论史',
        '44': '广东',
    }

    rules = (
        Rule(LinkExtractor(allow=list(map(lambda x: '.*post-{}'.format(x),
                                          url_keywords.keys()))), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=list(map(lambda x: '.*{}.*'.format(x),
                                          url_keywords.keys()))),
             follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['title'] = response.xpath(
            '//h1[@class="atl-title"]/span[@class="s_title"]/span/text()').extract_first()
        i['body'] = response.xpath(
            '//div[@class="bbs-content clearfix"]').extract_first()
        i['tags'] = response.xpath(
            '//div[@class="atl-location clearfix"]/p[@class="crumbs"]/em/a/text()').extract()
        i['source'] = '天涯社区'
        i['source_url'] = response.url
        try:
            i['datetime'] = int(tuple(map(lambda x: time.mktime(time.strptime(x.split('：')[-1], '%Y-%m-%d %H:%M:%S ')), filter(
                lambda x: '时间' in x, response.xpath('//div[@class="atl-menu clearfix js-bbs-act"]/div[@class="atl-info"]/span/text()').extract())))[0])
        except:
            i['datetime'] = 0

        if None not in i.values() and i['body'] != []:
            return i
