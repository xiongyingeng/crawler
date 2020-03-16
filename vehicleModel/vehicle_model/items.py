# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VehicleModelItem(scrapy.Item):
    # define the fields for your item here like:
    # 车名称
    name = scrapy.Field()

    # 车类型
    classify = scrapy.Field()

    # 报价
    price = scrapy.Field()
