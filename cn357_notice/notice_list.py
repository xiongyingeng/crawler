# -*- coding: utf-8 -*-
# @Time : 2020/8/25 15:18
# @Author : Will
# @Software: PyCharm
# 单线程处理

import os
import pandas as pd
from lxml import etree

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

logger.addHandler(handler)
logger.addHandler(console)

from req import Request


class NoticeListHandle(object):
    def __init__(self, save_path):
        self.base_url = "https://www.cn357.com"
        self.req = Request(logger)
        self.save_path = save_path

    def single_notice(self, notice):
        """单批次一页的数据"""
        save_filename = os.path.join(self.save_path, "公众型号各批次数据.csv")
        df, max_page = self.page_one(notice)
        logger.debug(f"url:{self.req.url},max page:{max_page}, page item:{len(df)}")
        df.to_csv(save_filename, encoding='utf-8-sig', index=False)
        for i in range(2, int(max_page) + 1):
            df_tmp, _ = self.page_one(notice + f"_{i}")
            df_tmp.to_csv(save_filename, mode='a', encoding='utf-8-sig', index=False, header=False)

    def page_one(self, notice):
        self.req.url = self.base_url + notice
        res = self.req.get()
        html = etree.HTML(res.text)
        row_href = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/@href")
        # title_row = html.xpath("//table[@class='listTable uiLinkList']/tr/th/text()")
        # a_text = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/text()")
        # row = html.xpath("//table[@class='listTable uiLinkList']/tr/td/text()")
        max_page = html.xpath("//span[@class='pageList']/a/text()")[-2]

        df = pd.read_html(res.text)[0]
        df['href'] = row_href

        return df, max_page

    def start(self):
        """公众型号批次列表"""
        self.req.url = self.base_url + "/notice_list/"
        res = self.req.get()
        if not res or res.status_code != 200:
            logger.error(f"{self.req.url}:{res}")
            return
        # html解析
        html = etree.HTML(res.text)
        result = html.xpath("//div[@class='lotList uiLinkList clear']//a/@href")

        for notice in result:
            self.single_notice(notice)


if __name__ == '__main__':
    save_path = "notice_list"
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    nlh = NoticeListHandle(save_path)
    nlh.start()
