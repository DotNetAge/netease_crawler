# -*- coding: utf-8 -*-

BOT_NAME = 'netease'

SPIDER_MODULES = ['netease_crawler.spiders']
NEWSPIDER_MODULE = 'netease_crawler.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPCACHE_ENABLED = True
TELNETCONSOLE_ENABLED = False

FEED_FORMAT = 'json'
FEED_URI = 'result.json'
FEED_EXPORT_ENCODING='utf-8'
