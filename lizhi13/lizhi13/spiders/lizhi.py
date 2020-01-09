# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from lizhi13.items import Lizhi13Item_title, Lizhi13Item_content

class LizhiSpider(CrawlSpider):
    name = 'lizhi'
    allowed_domains = ['lz13.cn']
    start_urls = ['https://www.lz13.cn/']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths="//div[@id='MainMenu']/ul/li/a"), callback='title_parse', follow=True),
    #     Rule(LinkExtractor(#allow="/lizhi/.*\.html",
    #                        restrict_xpaths="//div[@class='PostHead']//h3/a"),
    #          callback='content_parse', follow=True),
    # )
    def parse(self, response):
        mainmenus_list = response.xpath("//div[@id='MainMenu']/ul/li/a/@href").extract()
        for mainmenu in mainmenus_list:
            yield scrapy.Request(url=mainmenu, callback=self.title_parse)

    def title_parse(self, response):
        # 获取文章标题
        titles = response.xpath("//div[@class='PostHead']//h3/a/text()").extract()
        # 获取文章内容url
        content_urls = response.xpath("//div[@class='PostHead']//h3/a/@href").extract()

        for title in titles:
            item = Lizhi13Item_title()
            item['title'] = title
            yield item

        # 获取当前页内容
        for content_url in content_urls:
            yield scrapy.Request(url=content_url, callback=self.content_parse)

        # 获取与当前页相关的分页urls
        next_urls = Selector(response=response).xpath("//div[@class='pager']/a/@href").extract()
        for url in next_urls:
            yield scrapy.Request(url=url, callback=self.title_parse, dont_filter=False)#递归


    def content_parse(self, response):
        # print(response.url)
        divs = response.xpath("//div[@class='PostContent']")
        for div in divs:
            contents = div.xpath("p/strong/text()|p/strong/a/text()|p/text()|p/a/text()").extract()
            self.logger.info(div)
            for content in contents:
                item = Lizhi13Item_content()
                content = content.strip().replace('\u3000', '')
                if content:
                    item['content'] = content
                    yield item
