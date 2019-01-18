# -*- coding: utf-8 -*-
'''
@File  : handleCase.py
@Date  : 2019/1/15/015 18:24
'''
from common.parseExc import *
from common.config import CASEPATH
from common.log import Log


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
        checkPints = {}
        key, value = item.split(":")
        if "." in key:
            temp = {}
            key1 = (str(key).split("."))[0]  # payload.coin类型的集合点解析
            key2 = (str(key).split("."))[1]
            temp[key2] = value
            checkPints[key1] = temp
        else:
            checkPints[key] = value
        return checkPints

    # 处理每条用例的数据格式
    def handle_data(self, datas):
        global cid, describe, host, expect, method, params, checkPints
        if isinstance(datas, dict):
            # checkPints = {}
            cid = int(datas["caseId"])
            describe = str(quchu_n(datas["caseDescribe"]))
            host = str(quchu_n(datas["apiHost"]))
            expect = str(datas["expect"])
            method = str(datas["method"])
            params = str(datas["params"])
            if expect.split(";")[-1] !="":
                for item in expect.split(";"):
                    # key, value = item.split(":")
                    # if "." in key:
                    #     temp = {}
                    #     key1 = (str(key).split("."))[0]  # payload.coin类型的集合点解析
                    #     key2 = (str(key).split("."))[1]
                    #     temp[key2] = value
                    #     checkPints[key1] = temp
                    # else:
                    #     checkPints[key] = value
                    checkPints=self.handle_checkPoint(item)
            else:
                checkPints=self.handle_checkPoint(expect.replace(";", ""))
            datas["expect"] = checkPints
            return datas
        else:
            raise Exception("参数错误，所传参数datas必须是字典")

    # 获得所有测试用例
    def get_cases(self):
        cases = []
        rowValues = self.pe.get_row()[1:]
        for row in rowValues:
            if row[9] == "Y" or row[9] == "y" or row[9] == "":
                case = {}
                case["caseId"] = int(row[0])
                case["caseDescribe"] = quchu_n(str(row[1]))
                case["apiHost"] = quchu_n(str(row[2]))
                case["params"] = quchu_n(row[3])
                case["apiHeaders"]=quchu_n(row[4])
                case["method"] = quchu_n(row[5])
                case["relatedApi"] = quchu_n(row[6])
                case["relatedParams"] = quchu_n(row[7])
                case["expect"] = quchu_n(row[8])
                # case["isExecute"] = row[6]
                case = self.handle_data(case)
                cases.append(case)
            else:
                continue
        self.log.info("获取用例完毕，共获取用例{}条".format(len(cases)))
        return cases


if __name__ == '__main__':
    s=HandleCase().get_cases()
    print(s)
