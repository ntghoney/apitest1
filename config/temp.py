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


# for row in rowValues:
#     if row[10] == "Y" or row[10] == "y" or row[10] == "":
#         case = {}
#         case["caseId"] = int(row[0])
#         case["apiId"] = int(row[1])
#         case["caseDescribe"] = quchu_n(str(row[2]))
#         case["apiHost"] = quchu_n(str(row[3]))
#         case["params"] = quchu_n(row[4])
#         case["apiHeaders"] = quchu_n(row[5])
#         case["method"] = quchu_n(row[6])
#         if isinstance(row[7], float):
#             case["relatedApi"] = int(row[7])
#         else:
#             case["relatedApi"] = None
#         case["relatedParams"] = quchu_n(row[8])
#         case["expect"] = quchu_n(row[9])
#         # case["isExecute"] = row[6]
#         case = self.handle_data(case)
#         cases.append(case)
#     else:
#         continue
# self.log.info("获取用例完毕，共获取用例{}条".format(len(cases)))