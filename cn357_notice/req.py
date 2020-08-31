# -*- coding: utf-8 -*-
# @Time : 2020/8/25 17:30
# @Author : Will
# @Software: PyCharm

import requests
import time
import random


class Request(object):
    """http请求类"""

    def __init__(self, logger):
        self.logger = logger

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def get(self):
        # 请求
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                   "content-type": "text/html",
                   "content-encoding": "gzip",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Cache-Control": "max-age=1",
                   "Connection": "keep-alive"
                   }

        retry_times = 3
        i = 0
        time.sleep(random.uniform(1, 4))
        while True:
            try:
                self.logger.debug(self.url)
                res = requests.get(self.url, headers=headers)
                if res.ok:
                    break
                else:
                    self.logger.info(res.content)

                if i == retry_times:
                    time.sleep(random.uniform(1, 10))
                elif i > retry_times:
                    break
                else:
                    time.sleep(random.uniform(5, 20))
                i = i + 1
                self.logger.warning(f"retry times {i}, the max retry is {retry_times}")
            except Exception as e:
                self.logger.exception(repr(e))
                res = None
                break

        return res
