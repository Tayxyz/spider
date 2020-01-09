# -*- coding: utf-8 -*-
import scrapy
# from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ximalaya.items import XimalayaItem


class XimalayaNameSpider(CrawlSpider):
    name = 'ximalaya_name'
    allowed_domains = ['www.ximalaya.com']
    start_urls = ['https://www.ximalaya.com/category/']
    category_urls = 'https://www.ximalaya.com{category_url}'
    category_ids = 'https://www.ximalaya.com{category_id}'
    nextpage_urls = 'https://www.ximalaya.com{nextpage_url}'

    def parse(self, response):
        # 获取分类的url+id
        content = response.xpath("//div[@class='list _61P']/a/@href").extract()
        for url_id in content:
            yield scrapy.Request(url=self.category_urls.format(category_url=url_id),
                                 callback=self.category_parse)

    def category_parse(self, response):
        # print(response.url)
        # 获取总页上子页的url
        content = response.xpath("//div[@class='content']//li//a[@class='album-title line-1 lg bold _bkf']/@href").extract()
        for url_id in content:
            # print(self.category_ids.format(category_id=url_id))
            yield scrapy.Request(url=self.category_ids.format(category_id=url_id),
                                 callback=self.title_name_parse)
        # 获取分页的url
        next_pages = response.xpath("//div[@class='pagination-wrap']//a/@href").extract()
        for url in next_pages:
            yield scrapy.Request(url=self.nextpage_urls.format(nextpage_url=url), callback=self.category_parse)

    def title_name_parse(self, response):
        # 获取子页上的标题+主播
        title = response.xpath("//div[@class='info _II0L']/h1/text()").extract()[0]
        name = response.xpath("//p[@class='anchor-info-nick _RkQV']/a/text()").extract()[0]

        item = XimalayaItem()
        item['title_name'] = title + '\t' + name
        yield item
