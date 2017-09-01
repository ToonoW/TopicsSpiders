# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from scrapy import Request, settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from w3lib.html import remove_tags


class TopicsspidersPipeline(object):
    def process_item(self, item, spider):
        return item



class CollectImageUrlPipeline(object):
    """
    将body中的image URL取出存入image_urls待下载
    """
    def process_item(self, item, spider):
        body = item['body']
        urls = body.xpath('.//img').xpath('@src').extract()
        for url in urls:
            if 'http' not in url:
                if '//' in url:
                    index = urls.index(url)
                    urls[index] = 'http:' + url
                else:
                    logging.warning('图片URL不完整： {}', url)
                    urls.remove(url)
        item['image_urls'] = urls
        logging.info("图片数目: " + str(len(item['image_urls'])))
        return item


class ImagesDownloadPipeline(ImagesPipeline):
    # 下载图片
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            item['image_paths'] = []
        item['image_paths'] = image_paths
        return item


class MongoDBPipeline(object):
    """
    存储到MongoDB
    """

    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['body'] = remove_tags(item['body'].extract_first(), which_ones=('span', ))
        self.db[self.mongo_collection].insert(dict(item))


class DuplicatesPipeline(MongoDBPipeline):
    """
    初步去重
    """
    def process_item(self, item, spider):
        result = self.db[self.mongo_collection].find({'source_url': item['source_url']})
        if result.count() != 0:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item
