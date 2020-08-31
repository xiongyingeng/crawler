# -*- coding: utf-8 -*-
# @Time : 2020/8/31 10:23
# @Author : Will
# @Software: PyCharm

from sqlalchemy import create_engine
from queue import Queue
from notcie_list_multithreading import PageConsumer


def batch_pages(pages: list):
    # 页码处理

    # sqlite engine
    engine = create_engine('sqlite:///notice_details.db', echo=False)
    pages_queue = Queue()
    models_queue = Queue()
    pages_thread_num = 2

    thread_list = []

    for page in pages:
        pages_queue.put(str(page).strip().replace('\r', '').replace('\n', ''))

    for j in range(pages_thread_num):
        p = PageConsumer(pages_queue, models_queue, engine, "notice")
        p.start()
        thread_list.append(p)

    for thread in thread_list:
        thread.join()


def main(file: str):
    # 读取所有待处理的页码
    with open(file, mode='r') as ff:
        lines = ff.readlines()

    batch_pages(lines)


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    main(filename)
