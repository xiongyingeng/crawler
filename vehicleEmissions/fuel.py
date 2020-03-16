#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/1/7 15:57
# @Author : Will
# @Software: PyCharm
# 燃料消耗量信息爬取
# 中国汽车燃料消耗量查询系统:http://www.miit.gov.cn/asopCmsSearch/n2282/index.html?searchId=qcppcx

import random
import requests
import json
import datetime


class CrawlFuel:
    def __init__(self):
        self.url = "http://www.miit.gov.cn/asopCmsSearch/searchIndex.jsp?params=%257B%2522goPage%2522%253A{page}%252C%2522orderBy%2522%253A%255B%257B%2522orderBy%2522%253A%2522pl%2522%252C%2522" \
                   "reverse%2522%253Afalse%257D%255D%252C%2522pageSize%2522%253A10%252C%2522queryParam%2522%253A%255B%257B%2522shortName%2522%253A%2522" \
                   "allRecord%2522%252C%2522value%2522%253A%25221%2522%257D%255D%257D&callback=jsonp{time}&_={time_}"

        self.max_page = 1
        self.total_content_num = 0

    def page_one(self, index):
        """
        爬取一页数据
        :param index: 页码
        :return: 爬取的数据
        """
        ind = 0
        times = 3
        while ind < times:
            cur_time = int(time.time() * 1000)
            url = self.url.format(page=index, time=cur_time, time_=cur_time + random.randint(50, 200))
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                return response

            ind += 1

        return None

    def parse(self, response):
        """
        解析
        :return:
        """
        data = response.text
        start_pos = data.find("(")
        end_pos = data.rfind(")")
        dst = data[start_pos + 1:end_pos]
        js = json.loads(dst)
        self.max_page = js.get("totalPageNum")
        self.total_content_num = js.get("totalContentNum")

        dst = []
        result_list = js.get("resultMap")
        for result in result_list:
            # 生产企业
            produce_company = result.get("scqy")
            # 通用名称
            nick_name = result.get("tymc")
            # 车辆型号
            model = result.get("clxh")
            # 车辆种类
            v_kind = result.get("clzl")
            # 排量(ml)
            cc = result.get("pl")
            # 额定功率(kW)
            power = result.get("edgl")
            # 变速器类型
            transmission_type = result.get("bsqlx")
            # 市区工况 (L/100km)
            city_in = result.get("sqgk")
            # 市郊工况 (L/100km)
            city_out = result.get("sjgk")
            # 综合工况 (L/100km)
            nedc = result.get("zhgk")
            # 通告日期
            notice_date = result.get("tgrq")
            # 备案号
            ba_no = result.get("baID")
            # 最大设计总质量
            max_weight = result.get("zdsjzzl")
            # 整车整备质量
            total_weight = result.get("zczbzl")
            # 驱动型式
            eng_type = result.get("qdxs")
            # 燃料类型
            fire_type = result.get("rllx")
            # 国标
            national_standard = result.get("sygjbz")
            # 产地 （国产）
            produce_addr = result.get("clcd")

            # 备注
            remark = result.get("bz")

            dst.append((produce_company, nick_name, model, v_kind, cc, power, transmission_type, city_in, city_out, nedc, notice_date,
                        ba_no, total_weight, max_weight, eng_type, fire_type, national_standard, produce_addr, remark))

        return dst

    @staticmethod
    def process_item(items):
        """
        数据处理，保存文件or数据库等等
        :return:
        """
        import pandas as pd
        header_name = ['生产企业', '通用名称', '车辆型号', '车辆种类', '排量(ml)', '额定功率(kW)', '变速器类型', '市区工况 (L/100km)', '市郊工况 (L/100km)', '综合工况 (L/100km)', '通告日期',
                       '备案号', '整车整备质量', '最大设计总质量', '驱动型式', '燃料类型', '国标', '产地', '备注']
        pd.DataFrame(data=items, columns=header_name).to_csv("中国汽车燃料消耗量_{}.csv".format(str(datetime.datetime.today())[:10]), encoding='utf-8-sig', index=False)

    def start(self):
        """
        入口
        :return:
        """
        result = []
        cur_page = 1
        while True:
            print("爬取第{}页中……".format(cur_page))
            response = self.page_one(cur_page)
            result += self.parse(response)

            if cur_page == self.max_page:
                break
            else:
                cur_page += 1

            time.sleep(random.randint(1, 3))

        print("任务完成")
        self.process_item(result)


if __name__ == '__main__':
    import time

    start_time = time.time()
    craw = CrawlFuel()
    craw.start()
    print("花费时间：{}".format(time.time() - start_time))
