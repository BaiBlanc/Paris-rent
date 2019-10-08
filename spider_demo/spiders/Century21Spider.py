# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapy import log
import re

from spider_demo.items import SpiderDemoItem


class Century21Spider(scrapy.Spider):

    name = 'century'

    allowed_domains = ['zhipin.com']
    # Urls needed for the first round
    start_urls = ['https://www.century21.fr/annonces/location-appartement/v-paris/alentours-15/s-0-/st-0-/b-0-1400'
                  '/page-1/']

    def parse(self, response):
        print("parse start:")
        node_list = response.xpath('//div[@class="contentAnnonce"]')

        for node in node_list:
            item = SpiderDemoItem()
            # extract() will change xpath Objects to unicode strings
            # normalize-space() remove all the useless space and \n
            price = node.xpath('normalize-space(.//div[@class="price"]/text())').extract()
            type = node.xpath('normalize-space(.//h4[@class="detail_vignette"]/text())').extract()
            size = node.xpath('.//h4[@class="detail_vignette"]/text()[2]').extract()
            code_post = node.xpath('.//span[@class="font14"]/text()').extract()

            # Some reconstrustions and stocking into the fields of items
            price_match = re.match(r'\d+', re.sub(r'\s* ', '', price[0]))
            item['price'] = int(price_match.group())
            size_match = re.match(r'\d+\.\d+', re.sub(",", ".", size[0]))
            item['size'] = float(size_match.group())
            item['type'] = type[0]
            item['code_post'] = int(code_post[0])

            yield item
        # Potentially have the next page to spider iteravely
        next_url = response.xpath('.//li[@class="btnSUIV_PREC suivant"]/a/@href').extract()
        if next_url:
            next_url = "https://www.century21.fr"+next_url[0]
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback = self.parse,
                dont_filter = True
            )