# -*- coding: utf-8 -*-
# @Time : 2020/8/25 15:17
# @Author : Will
# @Software: PyCharm

"""
0、req.py  request请求页面
1、 notcie_list_multithreading.py 多线程爬取，注意爬取速度，网站有限制
2、 notice_list.py   单线程爬取页码，速度很慢
3、 query.py  从sqlite3查询，如vin查询品牌
4、 assign_page.py 指定页码数据请求，调用notcie_list_multithreading的pageone。一般用于请求失败项再次下载
5、 notice_detail.py 公众型号详细信息

增加一键错误处理更佳
"""
