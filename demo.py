# -*- coding: utf-8 -*-
'''
@File  : demo.py
@Date  : 2019/1/15/015 16:18
'''
from configparser import ConfigParser
import os
import json
import pytest_html



import requests
headers={"cookie":"_umdata=G1D9DFFBA554E65A731DFE539C75C23F93ACB10; Hm_lpvt_484788504bd0bc163a54b110d0dc003c=1547633889; Hm_lvt_484788504bd0bc163a54b110d0dc003c=1547632717,1547633889; DIS4=47cbc635e8c6402aa899522deb710a0f; lite_token=fe591551c125ba768d11c343a770baed; _uab_collina=154763271682458273515994; ln=1; lu=61984850; user_redirct_subtask_list=1",
         "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 version=2.0.2018101201 bid=com.he.ar",
         "Accept":"application/json"}
url="http://fp01.ops.gaoshou.me/s5/login.mobile"
url1="http://fp01.ops.gaoshou.me/s4/dashboard"
data={"phone":"17711794059","code":"123456"}
s=requests.post(url,data=data)
print(s.text)
# if "headers" not in cf.sections():
#     cf.add_section("headers")
# cf.set("headers","headers",h)
# with open("e:/project/ApiTest/config/conf.ini","w") as f:
#     cf.write(f)
#     f.close()
# cf.remove_option("headers","headers")
# with open("e:/project/ApiTest/config/conf.ini","w") as f:
#     cf.write(f)
#     f.close()
s="：12"
print("：" in s)