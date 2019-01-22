# -*- coding: utf-8 -*-
'''
@File  : config.py.py
@Date  : 2019/1/15/015 17:28
'''
import os,platform

# 测试环境域名
TESTDEV = "http://fp02.ops.gaoshou.me"
# TESTDEV = "http://www.baidu.com"

if platform.system()=="Windows":
    # 用例存放路径
    CASEPATH=os.path.dirname(__file__).replace("common","cases")+"\exmple.xlsx"
else:
    CASEPATH=os.path.dirname(__file__).replace("common","cases")+"/exmple.xlsx"






