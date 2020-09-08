# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:54
# @Author : Will
# @Software: PyCharm
# 多线程处理,并存储到sqlite3数据库
# 采用生产->消费模型
import os
import datetime
import random
import time
import pandas as pd
from sqlalchemy import create_engine
import threading
from queue import Queue

from lxml import etree
import logging

import gc

from req import Request

engine = create_engine("mysql+pymysql://root:root@192.168.70.91:3306/cn_notice_details?charset=utf8")

# 商车网
BASE_URL = "https://www.cn357.com"

log_path = "logs"
if not os.path.exists(log_path):
    os.mkdir(log_path)

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(os.path.join(log_path, "log_{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M"))))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d-%(levelname)s-%(message)s')
handler.setFormatter(formatter)

handler_err = logging.FileHandler(os.path.join(log_path, "log_{}_err.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M"))))
handler_err.setLevel(logging.ERROR)
formatter_err = logging.Formatter('%(asctime)s-%(message)s')
handler_err.setFormatter(formatter_err)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

logger.addHandler(handler)
logger.addHandler(console)
logger.addHandler(handler_err)


#
# lock = threading.Lock()


def recycling():
    # 强制进行垃圾回收
    gc.collect()


class Producer(threading.Thread):
    """公众号批次  记录每个批次有多少页"""

    def __init__(self, notice_queue, page_queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notices_queue = notice_queue
        self.pages_queue = page_queue
        self.req = Request(logger)

    def run(self) -> None:
        while not self.notices_queue.empty():
            notice = self.notices_queue.get(timeout=10)
            try:
                time.sleep(random.uniform(1, 3))
                self.pages(notice)
            except Exception as e:
                logger.exception("{}:{}".format(notice, str(e)))

        logger.debug('Producer finished!!!')

    def pages(self, notice):
        """单批次多少页的数据"""
        self.pages_queue.put(notice)
        max_page = self.page_one(notice)
        logger.debug(f"url:{self.req.url},max page:{max_page}")

        for i in range(2, int(max_page) + 1):
            self.pages_queue.put(notice + f"_{i}")

    def page_one(self, page) -> pd.DataFrame:
        """每一页数据解析"""
        self.req.url = BASE_URL + page
        res = self.req.get()
        html = etree.HTML(res.text)
        # row_href = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/@href")
        # title_row = html.xpath("//table[@class='listTable uiLinkList']/tr/th/text()")
        # a_text = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/text()")
        # row = html.xpath("//table[@class='listTable uiLinkList']/tr/td/text()")
        page_list = html.xpath("//span[@class='pageList']/a/text()")
        max_page = 0 if len(page_list) < 2 else page_list[-2]
        # df = pd.read_html(res.text)[0]
        # df['href'] = row_href
        #
        # # 保存每一个公众型号详细信息跳转的地址
        # for href in row_href:
        #     self.models_queue.put(href)

        return max_page


class PageConsumer(threading.Thread):
    """没一页的消费者，同时也是每个公众型号详细信息生产者"""

    def __init__(self, page_queue, models_queue, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages_queue = page_queue
        self.models_queue = models_queue
        self.engine = engine
        self.table_name = table_name
        self.req = Request(logger)

    def page_one(self, page) -> pd.DataFrame:
        """每一页数据解析"""
        self.req.url = BASE_URL + page
        res = self.req.get()
        if not res or res.status_code != 200:
            return None

        html = etree.HTML(res.text)
        row_href = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/@href")
        # title_row = html.xpath("//table[@class='listTable uiLinkList']/tr/th/text()")
        # a_text = html.xpath("//table[@class='listTable uiLinkList']/tr/td/a/text()")
        # row = html.xpath("//table[@class='listTable uiLinkList']/tr/td/text()")
        # max_page = html.xpath("//span[@class='pageList']/a/text()")[-2]

        df = pd.read_html(res.text)[0]
        df['href'] = row_href

        # 页码
        sp_list = page.split('_')
        page_id = 1 if len(sp_list) == 2 else sp_list[-1]
        df['page_id'] = page_id
        df.drop_duplicates(inplace=True)
        # 保存每一个公众型号详细信息跳转的地址
        for href in row_href:
            self.models_queue.put(href)

        return df

    def run(self) -> None:
        while not self.pages_queue.empty():
            page_id = self.pages_queue.get(timeout=10)
            try:
                time.sleep(random.uniform(1, 3))
                df = self.page_one(page_id)
                # lock.acquire()
                df.to_sql(self.table_name, self.engine, if_exists='append', index=False)
                # lock.release()
                del df
            except Exception as e:
                # 写入错误日志中
                logger.error(f"{page_id}-PageConsumer failure")
                logger.exception("{}:{}".format(page_id, str(e)))

        logger.debug('PageConsumer finished!!!')


class Consumer(threading.Thread):
    """消费者-每个公众型号对应的详细信息"""

    def __init__(self, model_queue, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.models_queue = model_queue
        self.engine = engine
        self.table_name = table_name

    def run(self) -> None:
        while not self.models_queue.empty():
            model = self.models_queue.get()
            try:
                time.sleep(random.uniform(1, 3))
                df_list = pd.read_html(BASE_URL + model)
                df = df_list[0]
                df_result = self.handle(df)
                # lock.acquire()
                df_result.to_sql(self.table_name, self.engine, if_exists='append', index=False)
                # lock.release()
                df_list.clear()
                logger.debug(f"{model} is succeed")
            except Exception as e:
                logger.error(f"Consumer failure-{model}")
                logger.warning("{}:{}".format(model, str(e)))

        recycling()
        logger.debug('Consumer finished!!!')

    def handle(self, df) -> pd.DataFrame:
        df_tmp = df.loc[1:20]
        df1 = df_tmp[[0, 1]].T
        df1.reset_index(inplace=True, drop=True)
        df2 = df_tmp[[2, 3]].T
        df2.reset_index(inplace=True, drop=True)
        df12 = pd.concat([df1, df2], axis=1)
        df12.columns = df12.iloc[0]
        del df_tmp
        return df12.loc[1:, :]


def req_notice_list(queue: Queue):
    """公众型号批次列表"""
    req = Request(logger)
    req.url = BASE_URL + "/notice_list/"
    res = req.get()
    if not res or res.status_code != 200:
        logger.error(f"{req.url}:{res}")
        return
    # html解析
    html = etree.HTML(res.text)
    result = html.xpath("//div[@class='lotList uiLinkList clear']//a/@href")

    for notice in result:
        queue.put(notice)


def main(batch=0):
    notices_queue = Queue()
    pages_queue = Queue()
    models_queue = Queue()

    notices_thread_num = 3
    pages_thread_num = 5
    models_thread_num = 8

    # engine = create_engine('sqlite:///notice_details.db', echo=False)

    if 0 == batch:
        # create notice list
        req_notice_list(notices_queue)
    else:
        # 指定批次处理
        notices_thread_num = 1
        notices_queue.put(f"/notice_{batch}")

    thread_list = []
    # 生成每批次每页的跳转url队列
    for i in range(notices_thread_num):
        p = Producer(notices_queue, pages_queue)
        p.start()
        thread_list.append(p)

    # 等待线程完成
    for thread in thread_list:
        thread.join()

    thread_list.clear()
    # 每批次每一页的处理，并生成每页公众号url队列
    for j in range(pages_thread_num):
        p = PageConsumer(pages_queue, models_queue, "notice")
        p.start()
        thread_list.append(p)

    # 等待线程完成
    for thread in thread_list:
        thread.join()

    time.sleep(10)
    # 处理详细信息
    for k in range(models_thread_num):
        c = Consumer(models_queue, "details")
        c.start()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("please input: 需要处理的批次 [0表示拉取所有批次的公众型号,会很慢]")
    batch = int(sys.argv[1])
    main(batch)
