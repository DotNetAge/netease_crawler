# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem


class NeteaseSpider(CrawlSpider):
    name = 'netease'
    allowed_domains = ['163.com']
    start_urls = ['https://www.163.com/']

    rules = (
        Rule(LinkExtractor(allow=r'(\w+):\/\/([^/:]+)\/(\d{2})+\/(\d{4})+\/(\d{2})+\/([^#]*)'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NewsItem()
        selector = Selector(response)
        item['title'] = selector.css('#epContentLeft>h1::text').get()

        item['pub_date'] = selector.css('#epContentLeft .post_time_source::text').get()
        if item['pub_date'] is not None:
            item['pub_date'] = item['pub_date'].split()[0]

        item['desc'] = selector.css('#epContentLeft .post_desc::text').get()
        if item['desc'] is not None:
            item['desc'] = item['desc'].strip()

        item['body'] = selector.css('#endText::text').get()
        if item['body'] is not None:
            item['body'] = item['body'].strip()

        item['link'] = response.url
        return item
