# -*- coding: utf-8 -*-
import scrapy


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        dd_list = response.xpath("//div[@class='mc']/dl/dd")
        item = {}
        for dt in dt_list:

            item["dt"] = dt.xpath("./a/text()")
            print(item["dt"])
        for dd in dd_list:
            em_list = dd.xpath("./em")
            # print(em_list)
            for em in em_list:
                item["em"] = em.xpath("./a/text()")
                item["em_href"] = em.xpath("./a/@href").extract()
                # print(["em_href"],item["em"])
                if item["em_href"] is not None:
                    item ["em_href"] = 'http:' + str(item["em_href"])
                    # print(item ["em_href"])
                yield scrapy.Request(item["em_href"], callback=self.em_parse)

    def em_parse(self,response):
        li_list = response.xpath(".//ul[@class='gl-warp']/li")
        print(li_list)
        for li in li_list:
            item['li_img'] = li.xpath(".//div[@class='p-img']/@href").extract()
            item['li_price'] = li.xpath(".//div[@class='p-price']//i/text()")
            print(item['li_price'])