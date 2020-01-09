# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from lizhi13.items import Lizhi13Item_content, Lizhi13Item_title

class Lizhi13Pipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Lizhi13Item_title):
            with open('title.txt', 'a', encoding='utf-8') as f:
                f.write(item['title'])
                f.write('\n')

        if isinstance(item, Lizhi13Item_content):
            content = item['content']

            f = open('content.txt', 'a', encoding='utf-8')
            f.write(content)
            f.write('\n')

        return item
