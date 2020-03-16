#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2019/12/26 11:17
# @Author : Will
# @Software: PyCharm
# vin 查询品牌
import time
import random
import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Vin2Brand:
    def __init__(self):
        self.start_url = "http://www.chinacar.com.cn/vin_index.html"
        self.browser = None

    def run(self, vin_list):
        # 设置页面不显示, 貌似卡着不动,还不如不设置快
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # self.browser = webdriver.Chrome(chrome_options=option)
        self.browser = webdriver.Chrome()

        result = []

        # 等待3秒，用于等待浏览器启动完成，否则可能报错
        time.sleep(3)
        self.browser.get(self.start_url)
        # 缓存,已经请求过的
        cache = {}
        for i, vin in enumerate(vin_list):
            print("第{ind}个vin匹配品牌……".format(ind=i + 1))
            if len(vin) != 17:
                continue
            left_vin = vin[:8]
            right_vin = vin[-8:]

            cache_vin = left_vin
            if cache_vin in cache:
                # 缓存中已有则直接找出
                ind = cache[cache_vin]
                values = result[ind][1:]
                result.append((vin,) + values)
            else:
                self.query(left_vin, right_vin)
                item = self.parse()
                result.append((vin,) + item)
                # 缓存
                cache[cache_vin] = i

        return result

    def parse(self):
        # 车辆型号	底盘型号	发动机型号	发动机生产商	发动机排量	发动机功率	燃烧种类	轴数	批次

        try:
            vehicle_models = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td//a').text
            chassis_type = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[2]').text
            eng_type = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[3]').text
            eng_producer = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[4]').text
            eng_cc = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[5]').text
            eng_power = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[6]').text
            burn_type = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[7]').text
            axis_nums = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[8]').text
            batch = self.browser.find_element_by_xpath('//table[@class="table-list"]//tbody//tr[@class="table-bg"]//td[9]').text
            return vehicle_models, chassis_type, eng_type, eng_producer, eng_cc, eng_power, burn_type, axis_nums, batch

        except NoSuchElementException:
            return ("",) * 9

    def query(self, left_vin_8, right_vin_8):
        """使用Selenium模拟浏览器模拟查询"""

        # 左8位
        left_vin = self.browser.find_element_by_xpath('//input[@id="leftvin"]')
        left_vin.clear()
        left_vin.send_keys(left_vin_8)
        # 右8位
        right_vin = self.browser.find_element_by_xpath('//input[@id="rightvin"]')
        right_vin.clear()
        right_vin.send_keys(right_vin_8)
        # 获取查询按钮
        commit = self.browser.find_element_by_xpath('//input[@src="/Public/gonggao_search/images/bottom.jpg"]')
        # 模拟单击查询按钮
        commit.click()

        # 等待浏览器完成
        time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    import sys
    import os

    filename = sys.argv[1]

    if os.path.exists(filename):
        save_filename = filename + ".csv"
        df = pd.read_csv(filename, encoding="utf-8-sig", low_memory=False)

        dst = Vin2Brand().run(df.VIN.values)
        if dst:
            df = pd.DataFrame(data=dst, columns=["VIN", "车辆型号", "底盘型号", "发动机型号", "发动机生产商", "发动机排量", "发动机功率", "燃烧种类", "轴数", "批次"])
            df.to_csv(save_filename, encoding='utf-8-sig', index=False)
            print("处理完毕！！！")
        else:
            print("没有正确的VIN！！！")
    else:
        dst = Vin2Brand().run([filename])[0]

        print("VIN:{0}\n车辆型号:{1}\n底盘型号:{2}\n发动机型号{3}\n发动机生产商:{4}\n发动机排量:{5}\n发动机功率:{6}\n燃烧种类:{7}\n轴数:{8}\n批次:{9}\n".format(
            dst[0], dst[1], dst[2], dst[3], dst[4], dst[5], dst[6], dst[7], dst[8], dst[9]
        ))

    sys.exit(0)
