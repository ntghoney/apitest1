# -*- coding: utf-8 -*-
'''
@File  : httputils.py
@Date  : 2019/1/15/015 17:04
'''
import requests, json
from common.config import TESTDEV


class Http(object):
    @classmethod
    def get(cls, path, params=None, headers=None):
        res = requests.get(TESTDEV + path, params=params, headers=headers)
        return res

    @classmethod
    def post(cls, path, params=None, headers=None):
        res = requests.post(TESTDEV + path, data=params, headers=headers)
        return res


if __name__ == '__main__':
    s = Http.get("/")
    a = requests.get("http://www.baidu.com")
    print(str(a.content))
    print("Response [200]" in str(a))
