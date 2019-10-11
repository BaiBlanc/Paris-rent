# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



import json
import scrapy


class DemoPipeline(object):

    def __init__(self):
        self.file = open('paris_rent_spider/data/data.json', 'w')

    def open_spider(self, spider):
        print("spider start")

    def process_item(self, item, spider):
        print("process start")
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"

        self.file.write(content)

        return item

    def close_spider(self, spider):
        self.file.close()
        print("spider closed")

