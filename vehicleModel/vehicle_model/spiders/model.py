# -*- coding: utf-8 -*-
import scrapy

from ..items import VehicleModelItem


class ModelSpider(scrapy.Spider):
    name = 'model'
    allowed_domains = ['car.bitauto.com']
    start_urls = ['http://car.bitauto.com/charlist.html']

    def parse(self, response):
        for info in response.xpath('//dl[@class="bybrand_list byletters_list"]/dd/ul/li'):
            item = VehicleModelItem()
            item['name'] = info.xpath('./div[@class="name"]/a/text()').extract_first()
            item['classify'] = info.xpath('./div[@class="name"]/a[@class="classify"]/text()').extract_first()
            item['price'] = info.xpath('./div[@class="bj"]/text()').extract_first()

            yield item
