# -*- coding: utf-8 -*-
'''
@File  : run.py
@Date  : 2019/1/15/015 18:45
'''
from common.handleCase import HandleCase
from common.report import Report
from common.httputils import Http
import time
from common.conDatabase import ConMysql, get_base_info
from common.log import Log
from common.report import get_now
import json
from common.parseConfig import ParseConfig, setPath
import string

pc = ParseConfig()
server_database = get_base_info(pc.get_info("ServerDatabase"))
con_server = ConMysql(server_database)  # 服务器数据库链接
con = ConMysql()  # 本地数据库连接对象


def write_headers(headers):
    pc.wirte_info("headers", "headers", headers)


# 从配置文件中获得默认headers
def get_default_headers():
    headers = {"cookie": pc.get_info("headers")["headers"]}
    return headers


# 检查期望与实际是否相匹配
def check(expect, fact, result, databaseResult="", databaseExpect=""):
    # 默认结果为pass
    result["ispass"] = "pass"
    # if fact.status_code == 200:
    try:
        response = fact.json()
        # 循环检查点与响应结果是否匹配
        temp = ""
        if not expect:
            result["ispass"] = "block"
            result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            result["reason"] = "检查点未设置"
            return
        if databaseResult and not databaseExpect:
            result["ispass"] = "block"
            result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            result["reason"] = "数据库检查点未设置"
            return
        if databaseExpect:
            if int(databaseExpect) == len(databaseResult):
                result["ispass"] = "pass"
                result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
            else:
                result["ispass"] = "fail"
                result["time"] = get_now().strftime("%Y/%m/%d %H:%M:%S")
                result["reason"] = "数据库检查失败，预期返回{}条数据，实际返回{}条数据".format(int(databaseExpect), len(databaseResult))

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
        result["reason"] = "程序出错：{}".format(str(e))
    return result


def run():
    global cid, describe, host, method, params, checkPints, con, relatedApi, relatedParams, apiInfo, sqlStatement, databaseExpect, sqlResult
    '''
    是否为第一条用例，每次执行是获取第一条用例执行的headers信息写入配置文件
    之后接口测试用例中如果headers信息为空，则自动调用配置文件中的headers信息
    '''
    defaultHeaders = get_default_headers()  # 头信息
    # 开始测试之前先清除数据库前一次测试储存的数据
    con.truncate_data("testCase")
    con.truncate_data("testResult")
    con.truncate_data("apiInfo")
    # 测试结果集
    resultSet = []
    log = Log()
    start_time = time.time()
    # 获取所有用例
    cases = HandleCase().get_cases()
    for case in cases:
        # 将用例存入数据库临时保存
        con.insert_data("testcase", **case)
        # 将接口数据插入数据库apiInfo表中暂时保存
        apiInfo = {"apiId": int(case["apiId"]), "apiHost": case["apiHost"], "apiParams": case["params"],
                   "method": case["method"], "relatedApi": case["relatedApi"], "relatedParams": case["relatedParams"]}
        # 如果数据库中不存在apiId的接口，则插入
        if not con.query_all("select * from apiInfo  where apiId={}".format(apiInfo["apiId"])):
            con.insert_data("apiInfo", **apiInfo)
    for case in cases:
        result = {}
        relatedApi = case["relatedApi"]
        relatedParams = case["relatedParams"]
        cid = case["caseId"]
        describe = str(case["caseDescribe"])
        host = str(case["apiHost"])
        checkPints = case["expect"]
        method = str(case["method"])
        params = str(case["params"])
        headers = case["apiHeaders"]
        sqlStatement = str(case["sqlStatement"])
        databaseExpect = case["databaseExpect"]
        result["caseId"] = cid
        result["caseDescribe"] = describe
        result["apiHost"] = host
        # 如果用例中headers信息没写，则调用配置文件中的headers信息
        if headers:
            headers = json.loads(headers, encoding="utf8")
        else:
            if host != "/s5/create_user":
                headers = defaultHeaders
            else:
                headers = ""
        if databaseExpect:
            result["databaseExpect"] = databaseExpect
        else:
            result["databaseExpect"] = " "
        if sqlStatement:
            sqlResult = con_server.query_all(sqlStatement)
        else:
            sqlResult = ""
        if sqlResult:
            result["databaseResult"] = str(sqlResult)
        else:
            result["databaseResult"] = " "
        if checkPints:
            result["except"] = str(checkPints)
        else:
            result["except"] = ""
        while True:
            if relatedApi is None:
                if method == "post":
                    if params:
                        params = string.Template(params)
                        params = params.substitute(vars())
                        result["apiParams"] = params
                        params = json.loads(str(case["params"]), encoding="utf8")
                    fact = Http.post(host, params=params, headers=headers)
                    result["fact"] = str(fact.text)
                    check(checkPints, fact, result, databaseExpect=databaseExpect,
                          databaseResult=sqlResult)
                    # 如果调用了creat_user的接口，就将接口的headers信息写入配置文件
                    if host == "/s5/create_user":
                        write_headers((str(fact.headers["Set-Cookie"])))
                else:
                    fact = Http.get(host, params=params, headers=headers)
                    result["fact"] = str(fact.text)
                    check(checkPints, fact, result, databaseExpect=databaseExpect,
                          databaseResult=sqlResult)
                    if host == "/s5/create_user":
                        write_headers((str(fact.headers["Set-Cookie"])))
                break
            relatedApiInfo = con.query_one("select * from apiInfo where apiId={}".format(relatedApi))
            relatedParams1 = relatedApiInfo["relatedParams"]
            apiHost = relatedApiInfo["apiHost"]
            relatedApi = relatedApiInfo["relatedApi"]
            apiParams = relatedApiInfo["apiParams"]
            apiMethod = relatedApiInfo["method"]
            if apiParams:
                apiParams = json.loads(str(apiParams), encoding="utf8")
            if apiMethod == "post":
                s = Http.post(apiHost, params=apiParams, headers=headers)
                if relatedParams:
                    var = locals()
                    var[relatedParams] = "8443"
            else:
                s = Http.get(apiHost, params=apiParams, headers=headers)
                if relatedParams.__eq__("headers"):
                    headers = {"cookie": str(s.headers["Set-Cookie"])}

        # 将执行结果写入数据库临时保存
        con.insert_data("testResult", **result)
        resultSet.append(result)
    end_time = time.time()
    time_consum = end_time - start_time  # 测试耗时
    case_count = con.query_all("SELECT caseId FROM testresult")  # 执行用例
    fail_case = con.query_all("SELECT caseId FROM testresult WHERE ispass='fail'")  # 执行失败的用例
    block_case = con.query_all("SELECT caseId FROM testresult WHERE ispass='block'")  # 执行阻塞的用例
    success_case = con.query_all("SELECT caseId FROM testresult WHERE ispass='pass'")  # 执行成功的用例
    if case_count is None:
        case_count = 0
    else:
        case_count = len(case_count)
    if fail_case is None:
        fail_case = 0
    else:
        fail_case = len(fail_case)
    if block_case is None:
        block_case = 0
    else:
        block_case = len(block_case)
    if success_case is None:
        success_case = 0
    else:
        success_case = len(success_case)
    result_info = "本次测试执行完毕，共耗时{}秒，共执行用例：{}条，成功：{}条，失败：{}条，阻塞：{}条".format(float("%.2f" % time_consum), case_count,

                                                                          success_case, fail_case, block_case)
    log.info(result_info)
    # 将测试结果写入测试报告
    report = Report()
    report.set_result_info(result_info)
    report.get_report(resultSet)
    # 关闭数据库
    con.close()
    con_server.close()


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
