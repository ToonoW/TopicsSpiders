import json
import re

from scrapy import Request
from scrapy.spiders import CrawlSpider


FOOD_CATEGORY_DICT = {
    '1': '主食',
    '2': '肉蛋',
    '3': '大豆及制品',
    '4': '蔬菜菌藻',
    '5': '水果',
    '6': '奶',
    '7': '油脂',
    '8': '坚果',
    '9': '调味',
    '10': '饮料',
    '11': '零食、点心和冷饮',
    '12': '其他',
}


class BooheeSpider(CrawlSpider):
    name = 'boohee'
    allowed_domains = ['boohee.com', ]
    start_urls = ['', ]

    def parse(self, response):
        """解析列表页
        解析列表页，请求列表的项目，若还有下一页则请求下一页，并且回调为本方法
        """
        data = json.loads(response.text)
        if data['page'] < data['total_pages']:
            # 存在下一页的发起请求下一页
            yield Request(
                re.sub(r'page=\d+', 'page=' +
                       str(data['page']+1), response.url.split('?')[0]),
                callback=self.parse,
            )

        # 获取分类代码
        category_value = re.findall(r'value=(\d+)', response.url)[0]
        for food in data['foods']:
            # 请求食品项目
            yield Request(
                'http://food.boohee.com/fb/v1/foods/' + food['code'],
                callback=self.parse_item,
                meta={'category_value': category_value},
            )

    def parse_item(self, response):
        data = json.loads(response.text)
        del data['id']
        del data['code']
        data['source_url'] = response.url
        data['category'] = FOOD_CATEGORY_DICT[response.meta['category_value']]
        return data
