# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TopicsspidersItem(scrapy.Item):

    title = Field()
    body = Field()
    source = Field()        # 来源名称
    source_url = Field()    # 来源URL
    datetime = Field()      # 时间
    image_urls = Field()    # 图片来源地址
    images = Field()        # 利用{index}进行占位，使用的时候替换上图片地址
    image_paths = Field()   # 图片路径列表
