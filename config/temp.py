# -*- coding: utf-8 -*-
'''
@File  : temp.py
@Date  : 2019/1/17/017 16:05
'''
# 判断接口是否调用成功，返回200
            # if fact.status_code == 200:
            #     response = fact.json()
            #     # 循环检查点与响应结果是否匹配
            #     temp = ""
            #     for key in checkPints.keys():
            #         if not isinstance(checkPints[key], dict):
            #             if not str(checkPints[key]) .__eq__(str(response[key])):
            #                 result["ispass"] = "fail"
            #                 result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            #                 temp+="{}的值预期为：{}，实际为：{}\n".format(key, checkPints[key],response[key])
            #                 result["reason"]=temp
            #             else:
            #                 result["ispass"] = "pass"
            #                 result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            #         else:
            #             for key1 in checkPints[key].keys:
            #                 if str(response[key][key1]).__eq__(str(checkPints[key][key1])):
            #                     result["ispass"] = "fail"
            #                     result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            #                     temp += "{}的值预期为：{}，实际为：{}\n".format(key, checkPints[key], response[key])
            #                     result["reason"] = temp
            #                 else:
            #                     result["ispass"] = "pass"
            #                     result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            # else:
            #     result["ispass"] = "fail"
            #     result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            #     result["reason"] = "网络连接错误或其他错误，接口返回{}".format(fact.status_code)