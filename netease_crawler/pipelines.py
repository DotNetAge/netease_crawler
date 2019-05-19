# -*- coding: utf-8 -*-

import pymongo
import logging
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class MongoDBPipeline(object):
    """
    MongoDB数据管道

    配置方法：
    ITEM_PIPELINES = ['netease_crawler.pipelines.MongoDBPipeline', ]

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "数据库名"
    MONGODB_COLLECTION = "表名"
    """

    def __init__(self, server=None, port=None, db_name=None, col=None):
        self.server = server
        self.port = port
        self.db_name = db_name
        self.col = col

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(self.server, self.port)
        self.db = self.connection[self.db_name]
        self.collection = self.db[self.col]

    def close_spider(self, spider):
        self.connection.close()

    @classmethod
    def from_crawler(cls, crawler):
        server = crawler.settings.get('MONGODB_SERVER'),
        port = crawler.settings.getint('MONGODB_PORT')
        db_name = crawler.settings.get('MONGODB_DB')
        collection_name = crawler.settings.get('MONGODB_COLLECTION')
        return cls(server, port, db_name, collection_name)

    def process_item(self, item, spider):
        if item['title'] is None:
            raise DropItem()

        self.collection.insert(dict(item))
        logger.debug("成功将数据插入至MongoDB", extra={'spider': spider})
        spider.crawler.stats.inc_value(
            'mongodb/inserted', spider=spider)
        return item
