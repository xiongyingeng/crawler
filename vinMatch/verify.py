#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2019/12/25 15:12
# @Author : Will
# @Software: PyCharm
# vin校验


def checksum(vin_str):
    """vin码校验, 成功返回200
    计算方法：VIN码从从第一位开始，码数字的对应值×该位的加权值，计算全部17位的乘积值相加除以11，所得的余数，即为第九位校验值
    """

    if len(vin_str) != 17:
        return -1

    # 内容的权值: VIN码各位数字的“对应值”：
    text_weight = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
        'G': 7, 'H': 8, 'I': 0, 'J': 1, 'K': 2, 'L': 3,
        'M': 4, 'N': 5, 'O': 0, 'P': 7, 'Q': 8, 'R': 9,
        'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7,
        'Y': 8, 'Z': 9
    }

    # 位置的权值: VIN码从第1位到第17位的“加权值”
    position_weight = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)

    # 校验位
    check_bit = vin_str[8]

    # 计算方法：VIN码从从第一位开始，码数字的对应值×该位的加权值，计算全部17位的乘积值相加除以11，所得的余数，即为第九位校验值.如果余数为10，则检验位为字母“X”
    weight_sum = 0
    for i, c in enumerate(vin_str):
        if c in text_weight:
            tw = text_weight.get(c)
        else:
            try:
                tw = int(c)
            except ValueError:
                return -2

        weight_sum += tw * position_weight[i]

    dst = divmod(weight_sum, 11)[1]

    if check_bit == 'X':
        if dst == 10:
            return 200
    else:
        try:
            if int(check_bit) == dst:
                return 200
            else:
                return dst
        except ValueError:
            return -3


if __name__ == '__main__':

    a = ['LZ91AE3A4J3LSA560',
         'LZ91AE3A5H1LSA511',
         'LZ91AE3A5J3LSA907',
         'LZ91AE3A7H2LSA360',
         'LZ91AE3A8J3LSA495',
         'LZ92RH3A4G1LSA027',
         'LZ932G3A0H1LSA014',
         'LZ932G3A0H1LSA062'
         ]

    for dd in a:
        print(checksum(dd))
