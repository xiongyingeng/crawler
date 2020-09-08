# -*- coding: utf-8 -*-
# @Time : 2020/8/27 17:07
# @Author : Will
# @Software: PyCharm
# sqlite 查询

import pandas as pd
from sqlalchemy import create_engine


class CarInfoQuery(object):
    def __init__(self):
        self.frame = None

    def init_db(self):
        # engine = create_engine(f'sqlite:///{self.db_name}')
        engine = create_engine("mysql+pymysql://root:root@192.168.70.91:3306/cn_notice_details?charset=utf8")
        self.frame = pd.read_sql('details', engine)
        self.frame.drop_duplicates(inplace=True)
        self.frame['pre_vin'] = self.frame['识别代号'].apply(lambda x: x if pd.isna(x) else x[:3])

    def query_by_vin(self, vin):
        """通过vin查询车辆信息"""
        df = self.frame.dropna(subset=['识别代号'])
        # 前3位一致，过滤减少查询量
        df_tmp: pd.DataFrame = df[df['pre_vin'] == vin[:3]].copy()

        result = None
        for index, row in df_tmp.iterrows():
            code_list = str(row['识别代号']).split(",")
            # vin_code = str(row['识别代号']).replace("×", "")
            for code in code_list:
                ind = str(code).find("×")
                if -1 == ind:
                    continue
                code = code[:ind]
                if code in vin:
                    result = row.to_dict()
                    break

        return result


if __name__ == '__main__':
    import sys

    vin = sys.argv[1]

    cq = CarInfoQuery()
    cq.init_db()
    res = cq.query_by_vin(vin)
    print(res)
