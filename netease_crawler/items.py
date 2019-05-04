# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class NewsItem(Item):
    title = Field()
    desc = Field()
    link = Field()
    pub_date = Field()
    body = Field()
