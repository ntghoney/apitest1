# -*- coding: utf-8 -*-
'''
@File  : handleCase.py
@Date  : 2019/1/15/015 18:24
'''
from common.parseExc import *
from common.config import CASEPATH
from common.log import Log
from common.config import CASENAME
import json


# 去掉换行符
def quchu_n(str):
    str = str.replace("\n", "")
    return str


class HandleCase(object):
    def __init__(self):
        # 实例parseExc对象
        self.log = Log()
        self.pe = PaserExc(CASEPATH, 0)

    # 总用例数
    def get_totals(self):
        return self.pe.get_nrows() - 1

    # 处理检查点中数据
    def handle_checkPoint(self, item):
        global key, value
        checkPints = {}
        key, value = item.split("=")
        if ":" in value:
            value = value.replace(":", "：")
        if "." in key:
            temp = {}
            key1 = (str(key).split("."))[0]  # payload.coin类型的集合点解析
            key2 = (str(key).split("."))[1]
            temp[key2] = value
            checkPints[key1] = temp
        else:
            checkPints[key] = value
        return checkPints

    def handle_related_params(self, item):
        global key, value
        related_params = {}
        key, value = item.split("=")
        if ":" in value:
            value = value.replace(":", "：")
        if "." in key:
            temp = {}
            key1 = (str(key).split("."))[0]  # payload.coin类型的集合点解析
            key2 = (str(key).split("."))[1]
            temp[key2] = value
            related_params[key1] = temp
        else:
            related_params[key] = value
        return related_params

    # 处理每条用例的数据格式
    def handle_data(self, datas):
        global cid, apiId, describe, host, expect, method, params, checkPints, relatedApi, relatedParams
        checkPints = {}
        # relatedParamsInfo = {}
        if isinstance(datas, dict):
            cid = int(datas["caseId"])
            apiId = int(datas["apiId"])
            describe = str(quchu_n(datas["caseDescribe"]))
            host = str(quchu_n(datas["apiHost"]))
            expect = str(datas["expect"])
            method = str(datas["method"])
            params = str(datas["params"])
            relatedParams = str(datas["relatedParams"])
            if expect:
                if expect.split(";")[-1] != "":
                    for item in expect.split(";"):
                        checkPints.update(self.handle_checkPoint(item))
                else:
                    checkPints = self.handle_checkPoint(expect.replace(";", ""))
                datas["expect"] = checkPints
            else:
                datas["expect"] = {}
            return datas
        else:
            raise Exception("参数错误，所传参数datas必须是字典")

    # 获得所有测试用例
    def get_cases(self):
        values = []
        cases = []
        result = []
        rowValues = self.pe.get_row()[1:]
        for row in rowValues:
            values.append(dict(zip(CASENAME, row)))
        # 去掉不执行的用例
        for case in values:
            if case["isExcute"] == "y" or case["isExcute"] == "Y" or case["isExcute"] == "":
                cases.append(case)
            case.pop("isExcute")
        # 转换用例字段的数据格式
        for case in cases:
            case["caseId"] = int(case["caseId"])
            case["apiId"] = int(case["apiId"])
            case["caseDescribe"] = quchu_n(str(case["caseDescribe"]))
            case["apiHost"] = quchu_n(str(case["apiHost"]))
            case["params"] = quchu_n(case["params"])
            case["apiHeaders"] = quchu_n(case["apiHeaders"])
            case["method"] = quchu_n(case["method"])
            if isinstance(case["relatedApi"], float):
                case["relatedApi"] = int(case["relatedApi"])
            else:
                case["relatedApi"] = None
            case["relatedParams"] = quchu_n(case["relatedParams"])
            case["expect"] = quchu_n(case["expect"])
            self.handle_data(case)
            result.append(case)
        return result


if __name__ == '__main__':
    s = HandleCase().get_cases()
    for i in s:
        print(i)
