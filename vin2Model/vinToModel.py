#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2020/1/7 15:57
# @Author : Will
# @Software: PyCharm
# vin查找对应车辆品牌等信息

import pandas as pd


class Vin2Model:
    def __init__(self):
        self.url = "http://www.fenco.cn/Index/search.html?word={vin}"

    def run_one(self, vin) -> tuple:
        try:
            url = self.url.format(vin=vin)
            df = pd.read_html(url)[0]
            data: pd.DataFrame = df[[1]]
            rs = data.T
            rs.insert(0, 'vin', vin)

            name = list(df[0].values)
            name.insert(0, 'vin')

            data_value = rs.iloc[0, :].to_list()
        except Exception as e:
            print(e)
            data_value, name = None, None

        return data_value, name

    def run(self, filename):
        result = []
        header = None
        i = 0
        with open(filename) as rf:
            for line in rf:
                i += 1
                print(f"第{i}个vin:{line}")
                line = line.strip()
                value, name = self.run_one(line)
                if value is None:
                    print(f"{line}失败")
                    continue
                else:
                    result.append(value)

                    if header is None:
                        header = name

            if result:
                pd.DataFrame(result, columns=name).to_csv("vin2model.csv", index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    import time
    import sys

    filename = sys.argv[1]
    start_time = time.time()
    vm = Vin2Model()
    vm.run(filename)

    print("花费时间：{}".format(time.time() - start_time))
