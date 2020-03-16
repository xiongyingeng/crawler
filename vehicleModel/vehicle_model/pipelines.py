# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class VehicleModelPipeline(object):
    def __init__(self):
        filename = "VehicleModel.csv"
        self.filer = open(filename, mode="w+", encoding="utf-8-sig")
        self.filer.write("型号,车辆分类,报价\n")

        # 用于关闭数据库资源

    def close_spider(self, spider):
        self.filer.close()

    def process_item(self, item, spider):
        """ 将数据写入sqlite数据库"""
        self.filer.write("{},{},{}\n".format(item['name'], item['classify'], item['price']))
