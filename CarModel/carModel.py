#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-28 12:12:19
# Project: carmodel
# pyspider 抓取车型， 已弃用
from pyspider.libs.base_handler import *
from fake_useragent import UserAgent
import pandas as pd
import time
import random

MODEL_URL = 'https://www.cn357.com/cvi.php?m=cvNotice&search=n&model='


def model_list(filename):
    # 获取车类型
    df = pd.read_table(filename, sep=",", header=None, encoding="utf-8-sig")
    return df[1].dropna().unique().tolist()


CAR_MODELS = model_list("C:\\Users\\Administrator\\Desktop\\dinran_static.txt")
print(len(CAR_MODELS))


class Handler(BaseHandler):
    ua = UserAgent()

    crawl_config = {
        "timeout": 120,
        "connect_timeout": 120,
        "retries": 3,
        "fetch_type": 'js',
        "auto_recrawl": True,
        "headers": {
            "User-Agent": ua.random
        },
    }

    @every(minutes=10 * 24 * 60)
    def on_start(self):
        for model in CAR_MODELS:
            self.crawl(MODEL_URL + model, callback=self.index_page, fetch_type='js', validate_cert=False)
            time.sleep(random.uniform(3, 10))

    @config(age=10)
    def index_page(self, response):
        for each in response.doc('div.gMain > ul > li > h3 > a').items():
            print(each.attr.href)
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js', validate_cert=False)
            break

    @config(priority=2)
    def detail_page(self, response):
        td_list = []
        for each in response.doc('div.gMain > table > tbody > tr > td').items():
            text = each.text()
            td_list.append(text if text else "NA")
        try:
            td_temp = td_list[0:-3]
            info = {td_temp[i]: td_temp[i + 1] for i in range(0, len(td_temp), 2)}
            info[td_list[-2]] = td_list[-1]

            info.update({"CAR_INFO": td_list[-3]})
            return info
        except:
            print(td_list)


if __name__ == '__main__':
    # filename = ""
    # with open(filename, "r", encoding='utf-8') as ff:
    #     file_rows = ff.readlines()
    #
    # notice_lst = model(file_rows)
    # result_url = notice(notice_lst)
    # td_list = ["企业名称", "吉利四川商用车有限公司", "企业地址", "南充市嘉陵区嘉南路一段180号", '发动机型号\n发动机生产企业\n发动机商标\n排量\n功率\nTZ280XSH10\n浙江艾麦电子科技有限公司\n0\n100', "备注", "fasfsa"]
    # td_list = ['变更(扩展)记录', '第314批第312批第310批第306批', '公告型号', 'DNC5046XXYBEV02', '公告批次', '314', '品牌', '远程', '类型', '纯电动厢式运输车', '额定质量', '1405,1340', '总质量', '4495',
    #            '整备质量', '2960', '燃料种类', '纯电动', '排放依据标准', 'NA', '轴数', '2', '轴距', '3360', '轴荷', '1800/2695', '弹簧片数', '3/3+3', '轮胎数', '6', '轮胎规格', '7.00R16 8PR', '接近离去角', '20/12',
    #            '前悬后悬', '1155/1480', '前轮距', '1590,1700', '后轮距', '1530', '识别代号', 'NA', '整车长', '5995', '整车宽', '2100', '整车高', '3150,3050', '货厢长', '4140,4100', '货厢宽', '2050,2010', '货厢高', '2080,2100,2000',
    #            '最高车速', '80', '额定载客', 'NA', '驾驶室准乘人数', '2,3', '转向形式', 'NA', '准拖挂车总质量', 'NA', '载质量利用系数', '0.51', '半挂车鞍座最大承载质量', 'NA',
    #            '企业名称', '吉利四川商用车有限公司', '企业地址', '南充市嘉陵区嘉南路一段180号', '电话号码', '08***48', '传真号码', '(0***70', '邮政编码', '637005', '底盘1', 'DNC1046BEVJ02', '底盘2', 'NA', '底盘3', 'NA', '底盘4', 'NA',
    #            '发动机型号\n发动机生产企业\n发动机商标\n排量\n功率\nTZ280XSH10\n浙江艾麦电子科技有限公司\n0\n100',
    #            '备注',
    #            '1:蓄电池为磷酸铁锂动力蓄电池,型号为:QJL04164-38-01,生产企业为:浙江钱江锂电科技有限公司,单体标称电压3.2V.标称容量:38Ah,蓄电池总标称电压:524.8V.2:驱动电机类型为:永磁同步电机,型号为:TZ280XSH10.额定功率为50kW,峰值功率为100kW.生产企业为浙江艾麦电子科技有限公司.3:驱动电机控制器型号为KTZ54X42SH12,生产企业为浙江艾麦电子科技有限公司.4:整车控制器型号为:Geely-VCU-HW01,生产企业为:吉利四川商用车有限公司.5:ABS型号:CM4XL-4S/4K(4S/4M),ABS生产企业:广州科密汽车电子控制技术股份有限公司.6:车厢顶部封闭不可开启.7:采用货厢裙部作侧防护(材质为玻纤增强聚丙烯蜂窝复合板或铝合金6061),采用货厢裙部作后防护(材质为Q235或铝合金6061).后部工作装置离地高度450mm.8:因货厢壁厚不同,具有两组货厢长宽尺寸,两组货厢尺寸只对应一组整车长宽外形尺寸,货厢内高与整车高对应关系:2100,2080对应3150,2000对应3050.9.选装货厢结构,选装前保险杠.10:辆配装车载终端.']

    # td_list = ['变更(扩展)记录', '第300批第296批第284批', '公告型号', 'BJ6610BG42BEV', '公告批次', '300', '品牌', '北京', '类型', '纯电动客车', '额定质量', 'NA', '总质量', '4432', '整备质量', '2928', '燃料种类', '纯电动', '排放依据标准', 'NA', '轴数', '2',
    #            '轴距',
    #            '3720', '轴荷', '1927/2505', '弹簧片数', '-/5', '轮胎数', '4', '轮胎规格', 'LT215/75R16', '接近离去角', '16/17', '前悬后悬', '1220/1135', '前轮距', '1655', '后轮距', '1650', '识别代号',
    #            'LPBMFC3A×××××××××,LPBMGC3A×××××××××', '整车长', '6075', '整车宽', '1885', '整车高', '2285', '货厢长', 'NA', '货厢宽', 'NA', '货厢高', 'NA', '最高车速', '100', '额定载客', '10-18', '驾驶室准乘人数', 'NA', '转向形式', 'NA',
    #            '准拖挂车总质量', 'NA', '载质量利用系数', 'NA', '半挂车鞍座最大承载质量', 'NA', '企业名称', '北京汽车制造厂有限公司', '企业地址', '北京市朝阳区东三环中路32号', '电话号码', '01***68', '传真号码', '(0***89', '邮政编码', '100020', '底盘1', '承载式车身', '底盘2',
    #            'NA',
    #            '底盘3', 'NA', '底盘4', 'NA', '发动机型号\n发动机生产企业\n发动机商标\n排量\n功率\nTZ238XSWT50ABJ\n北京汽车制造厂有限公司\n50', '备注',
    #            '电动机:峰值功率为100KW。ABS型号:TS80-3A4;ABS生产厂家:江苏盛昌隆联合科技有限公司。10-17座VIN为LPBMFC3A×××××××××,18座VIN为LPBMGC3A×××××××××。储能装置种类:磷酸铁锂蓄电池,储能装置总成生产企业:中天储能科技有限公司,技术阶段:发展期.']
    # td_temp = td_list[0:-3]
    # info = {td_temp[i]: td_temp[i + 1] for i in range(0, len(td_temp), 2)}
    # info[td_list[-2]] = td_list[-1]
    #
    # info.update({"CAR_INFO": td_list[-3]})
    #
    # print(info)
    pass
