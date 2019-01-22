# -*- coding: utf-8 -*-
'''
@File  : temp.py
@Date  : 2019/1/22/022 15:37
'''
# if relatedApi is None:
        #     if method == "post":
        #         fact = Http.post(host, params=params, headers=headers)
        #         result["fact"] = str(fact.text)
        #         check(checkPints, fact, result)
        #         # 如果是第一条用例，则将headers信息写入配置文件
        #         if is_first_case:
        #             write_headers((str(fact.headers["Set-Cookie"])))
        #     elif method == "get":
        #         fact = Http.get(host, params=params, headers=headers)
        #         result["fact"] = str(fact.text)
        #         check(checkPints, fact, result)
        #         if is_first_case:
        #             write_headers((lambda s: s.replace("\'", "\""))(str(fact.headers)))
        #     else:
        #         result["fact"] = "用例请求方法错误"
        #         result["ispass"] = "fail"
        #         result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
        #         result["reason"] = "用例错误，无法执行，没有{}请求方法".format(method)
        #         log.error("没有{}这种请求方式,请修改用例".format(method))
        #     result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
        # else:
        #     # temp=con.query_one("select * from apiInfo where apiId={}".format(relatedApi))