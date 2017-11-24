"""
豆瓣
"""
import time
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from TopicsSpiders.items import TopicsspidersItem
from w3lib.html import remove_tags

class DoubanSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/group/explore']

#    custom_settings = {
#        'DOWNLOAD_DELAY': 0.5,
#    }

    def parse(self, response):
        items = response.xpath('//div[@class="article"]/div/div[@class="channel-item"]')
        for item in items:
            title = item.xpath('div[@class="bd"]/h3/a/text()').extract_first()
            url = item.xpath('div[@class="bd"]/h3/a/@href').extract_first()
            yield Request(url, callback=self.parse_item, meta={'title': title})

        # 构造下一页
        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page_url = self.start_urls[0] + next_page
            yield Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = TopicsspidersItem()
        item['title'] = response.meta['title']
        item['body'] = response.xpath('//div[@class="topic-content"]')
        item['datetime'] = str(int(time.mktime(time.strptime(response.xpath('//span[@class="color-green"]/text()').\
                                                             extract_first(), '%Y-%m-%d %H:%M:%S'))))
        item['source'] = self.name
        item['source_url'] = response.url

        return item
