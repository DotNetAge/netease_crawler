# -*- coding: utf-8 -*-

BOT_NAME = 'netease'

SPIDER_MODULES = ['netease_crawler.spiders']
NEWSPIDER_MODULE = 'netease_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPCACHE_ENABLED = True
TELNETCONSOLE_ENABLED = False

#FEED_FORMAT = 'json'
#FEED_URI = 'result.json'
#FEED_EXPORT_ENCODING = 'utf-8'

REDIS_PORT = 6379
REDIS_DUP_DB = 0
# DUPEFILTER_CLASS = 'netease_crawler.dupefilters.RedisDupeFilter'    # Redis 过滤器
DUPEFILTER_CLASS = 'netease_crawler.dupefilters.RedisBloomDupeFilter' # Redis 布隆过滤器

MONGODB_SERVER = "localhost"	  # MongoDB 服务器地址
MONGODB_PORT = 27017		      # MongoDB 服务器的访问端口
MONGODB_DB = "netease"			  # MongoDB 采用的数据库名
MONGODB_COLLECTION = "articles"	  # 写入的集合名称

ITEM_PIPELINES = {
    'netease_crawler.pipelines.MongoDBPipeline': 300
}
