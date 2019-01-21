# -*- coding: utf-8 -*-
'''
@File  : run.py
@Date  : 2019/1/15/015 18:45
'''
from common.handleCase import HandleCase
from common.report import Report
from common.httputils import Http
import time
from common.conDatabase import ConMysql
from common.log import Log
from common.report import get_now
import json
from common.parseConfig import ParseConfig, setPath

pc = ParseConfig()


def write_headers(headers):
    pc.wirte_info("headers", "headers", headers)


# 从配置文件中获得默认headers
def get_default_headers():
    return pc.get_info("headers")


# 检查期望与实际是否相匹配
def check(expect, fact, result):
    # 默认结果为pass
    result["ispass"] = "pass"
    # if fact.status_code == 200:
    try:
        response = fact.json()
        # 循环检查点与响应结果是否匹配
        temp = ""
        for key in expect.keys():
            if not isinstance(expect[key], dict):
                # 判断检查点中的字段是否在响应结果中
                if key not in response.keys():
                    result["ispass"] = "fail"
                    result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
                    result["reason"] = "实际结果中没有{}这个字段,检查用例是否错误或接口返回结果错误".format(key)
                    return
                # 判断检查点中字段的值和返回结果字段的值是否一致
                if not str(expect[key]).__eq__(str(response[key])):
                    result["ispass"] = "fail"
                    result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
                    temp += "{}的值预期为：{}，实际为：{}\n".format(key, expect[key], response[key])
                    result["reason"] = temp
                else:
                    # 判断是否有检查点判断失败，如果有，ispass值仍然为fail
                    if result["ispass"].__eq__("fail"):
                        result["ispass"] = "fail"
                    else:
                        result["ispass"] = "pass"
                    result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            # 判断双重检查点，例如payload.message的形式
            else:
                for key1 in expect[key].keys:
                    if str(response[key][key1]).__eq__(str(expect[key][key1])):
                        result["ispass"] = "fail"
                        result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
                        temp += "{}的值预期为：{}，实际为：{}\n".format(key, expect[key], response[key])
                        result["reason"] = temp
                    else:
                        result["ispass"] = "pass"
                        result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
    except Exception as e:
        result["ispass"] = "fail"
        result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
        result["reason"] = "接口请求错误，状态码为：{}".format(fact.status_code)
    return result


def run():
    global cid, describe, host, method, params, checkPints, con, relatedApi, relatedPamras, apiInfo
    '''
    是否为第一条用例，每次执行是获取第一条用例执行的headers信息写入配置文件
    之后接口测试用例中如果headers信息为空，则自动调用配置文件中的headers信息
    '''
    is_first_case = True
    defaultHeaders = get_default_headers()  # 头信息
    # 数据库连接对象
    con = ConMysql()
    # 开始测试之前先清除数据库前一次测试储存的数据
    con.truncate_data("testCase")
    con.truncate_data("testResult")
    # 测试结果集
    resultSet = []
    log = Log()
    start_time = time.time()
    # 获取所有用例

    cases = HandleCase().get_cases()
    for case in cases:
        print(case)
        # 将用例数据插入数据库testCase表中暂时保存
        con.insert_data("testCase", **case)
        # 将接口数据插入数据库apiInfo表中暂时保存
        apiInfo = {"apiId": int(case["apiId"]), "apiHost": case["apiHost"], "apiParams": case["params"],
                   "relatedApi": case["relatedApi"], "relatedParams": case["relatedParams"]}
        # 如果数据库中不存在apiId的接口，则插入
        if not con.query_all("select * from apiInfo  where apiId={}".format(apiInfo["apiId"])):
            con.insert_data("apiInfo", **apiInfo)
        result = {}
        cid = case["caseId"]
        describe = str(case["caseDescribe"])
        host = str(case["apiHost"])
        checkPints = case["expect"]
        method = str(case["method"])
        params = str(case["params"])
        headers = case["apiHeaders"]
        # 如果用例中headers信息没写，则调用配置文件中的headers信息
        if headers == "":
            headers = defaultHeaders
        else:
            headers = json.loads(headers, encoding="utf8")
        if params is not "":
            params = json.loads(str(case["params"]), encoding="utf8")
        result["caseId"] = cid
        result["caseDescribe"] = describe
        result["apiHost"] = host
        result["except"] = str(checkPints)

        if method == "post":
            fact = Http.post(host, params=params, headers=headers)
            result["fact"] = str(fact.text)
            check(checkPints, fact, result)
            # 如果是第一条用例，则将headers信息写入配置文件
            if is_first_case:
                write_headers((lambda s: s.replace("\'", "\""))(str(fact.headers)))

        elif method == "get":
            fact = Http.get(host, params=params, headers=headers)
            result["fact"] = str(fact.text)
            check(checkPints, fact, result)
            if is_first_case:
                write_headers((lambda s: s.replace("\'", "\""))(str(fact.headers)))
        else:
            result["fact"] = "用例请求方法错误"
            result["ispass"] = "fail"
            result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            result["reason"] = "用例错误，无法执行，没有{}请求方法".format(method)
            log.error("没有{}这种请求方式,请修改用例".format(method))
        result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
        # 将执行结果写入数据库临时保存

        con.insert_data("testResult", **result)
        resultSet.append(result)
        is_first_case = False
    # 将测试结果写入测试报告
    report = Report()
    report.get_report(resultSet)
    # 关闭数据库
    con.close()


if __name__ == '__main__':
    # data = {"phone": "17711794059", "code": "123456"}
    # s = Http.post("/s5/login.mobile", params=data)
    #
    # print(type(s.json()))
    #
    # s = HandleCase().get_cases()[0]
    # c = dict(s["expect"])
    # for key in c.keys():
    #
    #     nt(key)
    # s = "是dfdsfds发的规范的施工的双方各地方个的双方各得十分个收到"
    run()
