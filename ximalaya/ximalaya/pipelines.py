# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from ximalaya.items import XimalayaItem

class XimalayaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, XimalayaItem):
            with open('title_name.txt', 'a', encoding='utf-8') as f:
                f.write(item['title_name'])
                f.write('\n')

        return item
