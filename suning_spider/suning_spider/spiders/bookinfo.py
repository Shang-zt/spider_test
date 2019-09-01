# -*-coding: utf-8 -*-
from scrapy import spiders as spiderss
import scrapy


class BookSpider(spiderss):
    name = 'bookinfo' \
           ''
    allowed_domains = ['suning.com']
    start_urls = ['http://book.suning.com']

    def parse(self,response):
        div_list = response.xpath("//div[@class='menu-list']/div")
        for div in div_list:
           item = {}
           item["b1"] = div.xpath("./div[1]//h3/a/text()").extract_first()
           b1_list = div.xpath(".dl/dd/a")
           for i in b1_list:
               item["s_href"] = i.xpath("./@href").extract_first()
               item["s_cate"] = i.xpath("./text()").extract_first()
               if item["s_href"] is not None:
                   item["s_href"] = item["s_href"]
                   yield scrapy.Request(
                       item["s_href"],
                       callback=self.parse_book_list,
                       meta = {"item":item}
                   )

    def parse_book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//div[@class='filter-results productMain clearfix  temporary']/ul/li")
        for li in li_list:
            item['book_name'] = li.xpath(".//p[@class='sell-point']/a/@alt")
            item['book_img'] = li.xpath(".//div[@class='img-block']/a/@src")
            item['book_price'] = li.xpath(".//div[@class='res-info']/p/em/text()")
