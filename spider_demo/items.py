# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderDemoItem(scrapy.Item):
    # defining the fields
    size = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    code_post = scrapy.Field()
    info = scrapy.Field()