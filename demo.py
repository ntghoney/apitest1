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
headers={"cookie":'DIS4=f3002ea4638a4b8b902b4da0a9c882b8; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, lu=26; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, ln=1; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/',
         # "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 version=2.0.2018101201 bid=com.he.ar",
         # "Accept":"application/json"
         }
url="http://fp02.ops.gaoshou.me/s5/login.mobile"
url1="http://fp02.ops.gaoshou.me/s4/dashboard"
url2="http://fp02.ops.gaoshou.me/s5/create_user"
url3="http://fp02.ops.gaoshou.me/s4/bindMobile"
url4="http://fp01.ops.gaoshou.me/a/5.0/bindMobile.occupied"

data={"phone":"17711794055","code":"4883"}
data3={"phone":"17711794050","code":"123456"}
s4=requests.post(url2)
h={'Server': 'nginx', 'Date': 'Tue, 22 Jan 2019 03:11:05 GMT', 'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Vary': 'Accept-Encoding', 'cookie': 'DIS4=f3002ea4638a4b8b902b4da0a9c882b8; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, lu=26; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, ln=1; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true', 'X-Diablo-Revision': 'cd7ee62', 'X-Hebe-Host': 'h1571', 'X-Qk-Lb-Overloading-Level': '0', 'Content-Encoding': 'gzip'}

# print(s4.headers)
# s5=requests.post(url3,data=data3,headers=headers)
# print(s5.text)
# print(s4.headers)
#Set-Cookie
#DIS4=8ab9c1277d2141148369de04857578b7
s=requests.post(url,data=data)
print(s.headers)
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
{'caseId': 2, 'apiId': 1, 'caseDescribe': '缺少phone参数', 'apiHost': '/s4/login.mobile', 'params': '{"code":"123456"}', 'apiHeaders': '', 'method': 'post', 'relatedApi': '', 'relatedParams': '', 'expect': {'err_code': '0', 'err_msg': '缺少参数：phon'}}
