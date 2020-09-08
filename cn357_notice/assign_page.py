# -*- coding: utf-8 -*-
# @Time : 2020/8/31 10:23
# @Author : Will
# @Software: PyCharm
# 爬取指定某些个批次的页码

from queue import Queue
from notice_list_multithreading import PageConsumer, Consumer


def batch_pages(pages: list):
    # 页码处理

    pages_queue = Queue()
    models_queue = Queue()
    pages_thread_num = 5
    models_thread_num = 8

    thread_list = []

    for page in pages:
        pages_queue.put(str(page).strip().replace('\r', '').replace('\n', ''))

    for j in range(pages_thread_num):
        p = PageConsumer(pages_queue, models_queue, "notice")
        p.start()
        thread_list.append(p)

    for thread in thread_list:
        thread.join()

    for k in range(models_thread_num):
        c = Consumer(models_queue, "details")
        c.start()


def main(file: str):
    # 读取所有待处理的页码
    with open(file, mode='r') as ff:
        lines = ff.readlines()

    batch_pages(lines)


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    main(filename)
