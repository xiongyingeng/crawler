# -*- coding: utf-8 -*-
# @Time : 2020/8/31 10:56
# @Author : Will
# @Software: PyCharm

# 公众型号详细信息
import time
import pandas as pd
from sqlalchemy import create_engine
from queue import Queue

from notcie_list_multithreading import logger, Consumer

engine = create_engine('sqlite:///notice_details.db', echo=False)


# 计算函数耗时
def run_time_back(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        logger.debug('current function [%s] start...' % func.__name__)
        result = func(*args, **kw)
        logger.debug('current function [%s] run time is %.2fs' % (func.__name__, time.time() - local_time))
        return result

    return wrapper


def detail(models_queue):
    # sqlite engine
    pages_thread_num = 3

    thread_list = []
    for j in range(pages_thread_num):
        p = Consumer(models_queue, engine, "details")
        p.start()
        thread_list.append(p)

    for thread in thread_list:
        thread.join()


@run_time_back
def read_db():
    frame = pd.read_sql('notice', engine)
    frame.info()
    return frame


def main():
    models_queue = Queue()
    frame = read_db()

    for ind, row in frame['href'].items():
        models_queue.put(row)

    detail(models_queue)


if __name__ == '__main__':
    main()
