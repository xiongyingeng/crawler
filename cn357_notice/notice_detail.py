# -*- coding: utf-8 -*-
# @Time : 2020/8/31 10:56
# @Author : Will
# @Software: PyCharm

# 爬取指定文件的公或者notice表中的众型号详细信息
import time
import pandas as pd
from queue import Queue

from notice_list_multithreading import logger, Consumer, get_sql_conn


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
    pages_thread_num = 10

    thread_list = []
    for j in range(pages_thread_num):
        p = Consumer(models_queue, "details")
        p.start()
        thread_list.append(p)

    for thread in thread_list:
        thread.join()


@run_time_back
def read_db():
    engine = get_sql_conn()
    frame = pd.read_sql('notice', engine)
    engine.dispose()
    return frame


def main(file=0):
    models_queue = Queue()

    if 0 == file:
        frame = read_db()
    else:
        frame = pd.read_csv(file, encoding='utf-8-sig')

    for ind, row in frame['href'].items():
        models_queue.put(row)

    del frame
    detail(models_queue)


def detail_by_batch(batch_no):
    """按批次查询"""
    models_queue = Queue()
    engine = get_sql_conn()
    sql = "SELECT href FROM notice WHERE `批次`='第{}批'".format(batch_no)
    logger.debug(sql)
    frame = pd.read_sql(sql, engine)
    logger.debug("当前是第{}批次,公众型号数{}".format(batch, len(frame)))
    for ind, row in frame['href'].items():
        models_queue.put(row)

    del frame
    detail(models_queue)


if __name__ == '__main__':
    import sys
    import os

    print("please input filename or nothing[default pull all models]")
    filename = "test.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print("filename:{} not exists.".format(filename))
            if len(sys.argv) > 2:
                # 从某个批次开始直到批次为1，批次号递减
                start_batch = int(filename)
                if sys.argv[2] == 'all':
                    for batch in range(start_batch, 0, -1):
                        detail_by_batch(batch)
                        time.sleep(30)
            else:
                batch = int(filename)
                detail_by_batch(batch)
            exit(0)
        else:
            main(filename)
    else:
        main(filename)
