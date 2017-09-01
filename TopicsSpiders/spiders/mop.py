import json
import logging
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from TopicsSpiders.items import TopicsspidersItem


class MopSpider(CrawlSpider):

    MOP_API = 'http://h5listinterface.mop.com/wapmdi/data.html?colid=100001&pgsize=50&serialnum=300000&startcol='
    START_COLID = 9999

    name = 'mop'
    allowed_domains = ['mop.com']

    def start_requests(self):
        yield Request(self.make_api_url())

    def parse(self, response):
        result = {}
        try:
            result = json.loads(response.body)
        except:
            AttributeError('输入json出错')
            logging.error('输入json出错')
            logging.error(response.body)
        data = result.get('data')
        if data is None:
            data = []
        if len(data) is not 0:
            for page in data:
                info = {
                    'title': page['title'],
                    'datetime': page['cts'] // 1000,
                }
                yield Request('http://mdzh.mop.com/a/'+page['htmlname'], callback=self.parse_item, meta={'info': info})

            # 构造下一页
            next_page = self.make_api_url()
            yield Request(next_page, self.parse)

    def parse_item(self, response):
        info = response.meta['info']
        item = TopicsspidersItem()
        for key in info:
            item[key] = info[key]
        # 等待处理body中的图片链接
        item['body'] = response.xpath('//div[@class="post-content"]')
        item['source'] = self.name
        item['source_url'] = response.url

        return item

    def make_api_url(self):
        url = self.MOP_API + str(self.START_COLID)
        self.START_COLID = self.START_COLID + 50
        return url