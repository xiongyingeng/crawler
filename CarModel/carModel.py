#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# !@Time     :2019/3/28 17:46
# !@Author   :will
# 通过车类型获取车信息, 线程池获取
import os
import requests
import time
import random
from fake_useragent import UserAgent
import pandas as pd
import numpy as np
from lxml import etree

MODEL_URL = 'https://www.cn357.com'


def model_list(filename):
    # 获取车类型
    df = pd.read_table(filename, sep=",", header=None, encoding="utf-8-sig", low_memory=False)
    return df[0].dropna().unique().tolist()


def get(url):
    # 请求
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    retry_times = 3
    i = 0
    print(url)
    time.sleep(random.uniform(1, 4))
    while True:
        try:
            res = requests.get(url, headers=headers)
            if res.ok:
                break
            else:
                print(res.content)

            if i == retry_times:
                time.sleep(random.uniform(1, 10))
            elif i > retry_times:
                break
            else:
                time.sleep(random.uniform(5, 20))

            i = i + 1
        except Exception as e:
            print(repr(e))
            res = None
            break

    return res


def car_model_url(model):
    # 获取车类型url
    res = get(MODEL_URL + '/cvi.php?m=cvNotice&search=n&model=' + model)
    if not res:
        return

    if res.ok:
        # 解析页面
        html = etree.HTML(res.text)
        result = html.xpath("//div[@class='gMain']//ul/li/h3/a/@href")
        if result:
            return model, notice(result[0])
        else:
            return model, None


def try_find_child(element):
    children = element.getchildren()
    if len(children):
        if children[0].tag == 'a':
            return children[0].text
        return element.text
    else:
        return element.text


def notice(notice_url):
    res = get(MODEL_URL + notice_url)
    if not res:
        return None

    if res.ok:
        # 解析页面
        dst = []
        html = etree.HTML(res.text)
        property_lst = html.xpath("//div[@class='gMain']/table//tr/td")
        for e in property_lst:
            text = str(try_find_child(e)).strip().replace("\r\n", "").replace("\n", ",").replace("\r", "")
            dst.append(text if text else "")

        if dst[-12] == "发动机型号":
            # 可能不存在,暂时直接不存
            # tmp_list = dst[-12:-2]
            # for i in range(5):
            #     # 包含发动机型号,
            #     tmp_list.insert(2 * i + 1, tmp_list[2 * i + 5])
            # tmp_list = tmp_list[0:10]
            return dst[2:-13] + dst[-2:]
        else:
            return dst[2:]


def save(filename, resultslist):
    # 将结果写入文件

    print('start  write filename={}, filelines= {}'.format(filename, len(resultslist)))
    curlen = 0
    with open(filename, 'w', encoding='utf_8_sig') as file:
        for row in resultslist:
            curlen += 1
            if 0 == len(row):
                continue
            dst = ''
            for i in range(len(row)):
                if row[i] is not None:
                    dst += '%s' % row[i]
                dst += '|'

            dst = dst[0:-1] + '\n'
            file.write(dst)
    print('finish write filename={}'.format(filename))


def run(filepath):
    # 获取车型
    car_list = model_list(filepath)
    # car_list = ["JX7006BEV", "YTK6118GEV", "VCD7204C31PPHEV", "SQJ6460M1BEV"]
    # car_list = ['SX5040XXYBEV331S']

    if len(car_list) < 20:
        thread_num = 1
    else:
        thread_num = 10
    print("总共车类型数：{}, 线程数：{}".format(len(car_list), thread_num))
    from concurrent.futures import ThreadPoolExecutor, as_completed
    with ThreadPoolExecutor(thread_num) as pool:  # 生成线程池
        futures = []
        for model in car_list:
            # 线程处理
            futures.append(pool.submit(car_model_url, model))

        head = None
        value = []
        print("已全部加入线程池")
        t = time.time()
        count = 0
        for future in as_completed(futures):
            try:
                count += 1
                print("总车型数:{},已爬取车型数:{},待爬取车型数:{}".format(len(car_list), count, len(car_list) - count))
                model, data = future.result()
                if head is None:
                    head = [data[i] for i in range(len(data)) if i % 2 == 0]
                    head.insert(0, "vin")

                tmp = [data[i] for i in range(len(data)) if i % 2 == 1]
                tmp.insert(0, model)
                value.append(tmp)
            except Exception as exc:
                print(repr(exc))
                continue
        print("已完成爬取")
        if value:
            dir_path = os.path.dirname(filepath)
            base_name = os.path.basename(filepath).rsplit(".", 1)[0]
            save_path = os.path.join(dir_path, str(base_name) + "-cvi.csv")
            try:
                numpy_list = np.asarray(value)
                pd.DataFrame(numpy_list, columns=head).to_csv(save_path, index=False, sep='|')
            except:
                if head is not None:
                    value.insert(0, head)
                save(save_path, value)

        print("花费时长:", time.time() - t)


def run_single(filepath):
    car_list = model_list(filepath)
    value = []
    head = None
    t = time.time()
    for model in car_list:
        model, data = car_model_url(model)
        if head is None:
            head = [data[i] for i in range(len(data)) if i % 2 == 0]
            head.insert(0, "vin")

        tmp = [data[i] for i in range(len(data)) if i % 2 == 1]
        tmp.insert(0, model)
        value.append(tmp)

    print("已完成爬取")
    if value:
        dir_path = os.path.dirname(filepath)
        base_name = os.path.basename(filepath).rsplit(".", 1)[0]
        save_path = os.path.join(dir_path, str(base_name) + "-cvi.csv")
        try:
            numpy_list = np.asarray(value)
            pd.DataFrame(numpy_list, columns=head).to_csv(save_path, index=False, sep='|')
        except:
            if head is not None:
                value.insert(0, head)
            save(save_path, value)

    print("花费时长:", time.time() - t)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("pls input a file!!")
        exit(2)
    filename = sys.argv[1]
    print(filename)
    # run(filename)
    run_single(filename)
