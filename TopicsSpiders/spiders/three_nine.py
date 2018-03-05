# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ThreeNineSpider(CrawlSpider):
    """39健康网"""

    name = 'three_nine'
    allowed_domains = ['bbs.39.net', ]
    start_urls = ['http://bbs.39.net/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'TopicsSpiders.middlewares.MyAgentMiddleware': 544,
        }
    }

    rules = (
        Rule(LinkExtractor(allow=[r'.*/(\d+).html', ], deny=r'.*/user/.*'),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=('.*',),), follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        i = {}
        i['title'] = response.xpath(
            '//a[@name="atitle"]/text()').extract_first()
        i['body'] = response.xpath('//div[@class="main"]').extract_first()
        try:
            i['tags'] = (response.xpath(
                '//span[@class="link"]/a/text()').extract()[-1],)
        except:
            pass
        i['source'] = '39健康论坛'
        i['source_url'] = response.url

        try:
            i['datetime'] = int(time.mktime(time.strptime(response.xpath(
                '//span[@class="time"]/text()').extract_first(), '%Y-%m-%d %H:%M')))
        except:
            i['datetime'] = 0
        return i
