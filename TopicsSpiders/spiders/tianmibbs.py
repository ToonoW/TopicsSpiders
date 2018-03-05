# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TianmibbsSpider(CrawlSpider):
    """ 
    增加栏目的时候需要将栏目的列表页URL填入 start_urls 数组中，并将URL特征码填入下面的字典
    """

    name = 'tianmibbs'
    allowed_domains = ['bbs.tnbz.com']
    start_urls = ['http://bbs.tnbz.com/forum-9-1.html']

    url_keywords = {
        '9': '心情驿站',
    }

    rules = (
        Rule(LinkExtractor(allow=list(
            map(lambda x: '.*forum-{}-.*'.format(x), url_keywords.keys()))), follow=True),
        Rule(LinkExtractor(allow=r'.*thread-.*-1-.*'),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        i = {}
        i['title'] = response.xpath(
            '//span[@id="thread_subject"]/text()').extract_first()
        i['body'] = response.xpath('//td[@class="t_f"]').extract_first()
        i['tags'] = response.xpath(
            '//div[@id="pt"]/div[@class="z"]/a/text()').extract()[-2]
        i['source'] = '甜蜜家园'
        i['source_url'] = response.url

        try:
            i['datetime'] = int(time.mktime(time.strptime(response.xpath(
                '//div[@class="authi"]/em/span/@title').extract_first(), '%Y-%m-%d %H:%M:%S')))
        except:
            i['datetime'] = response.xpath(
                '//div[@class="authi"]/em/text()').extract_first()
            if i['datetime'] is not None:
                i['datetime'] = int(time.mktime(time.strptime(
                    ' '.join(i['datetime'].split()[-2:]), '%Y-%m-%d %H:%M:%S')))
            else:
                i['datetime'] = 0
        return i
