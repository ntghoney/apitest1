# -*- coding: utf-8 -*-
'''
@File  : test.py
@Date  : 2019/1/17/017 9:39
'''
import pytest
import json


def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5


a ='{"phone":"17711794059","code":"123456"}'
print(type(json.loads(a)))
