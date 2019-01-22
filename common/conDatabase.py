# -*- coding: utf-8 -*-
'''
@File  : conDatabase.py
@Date  : 2019/1/18/018 9:35
'''
import pymysql
from common.parseConfig import ParseConfig
from common.log import Log
import json

log = Log()


def get_base_info():
    mysqlInfo = ParseConfig().get_info("database")
    for key in mysqlInfo.keys():
        if key.__eq__("port"):
            mysqlInfo[key] = int(mysqlInfo[key])
    return mysqlInfo


# 将数据转换成字典形式储存
def data_for_dict(data):
    if len(data) == 8:
        data_dic = {}
        data_dic["caseId"] = int(data[0])
        data_dic["caseDescribe"] = str(data[1])
        data_dic["apiHost"] = str(data[2])
        data_dic["params"] = data[3]
        data_dic["method"] = data[4]
        data_dic["relatedApi"] = data[5]
        data_dic["relatedParams"] = data[6]
        data_dic["expect"] = json.loads(data[7])
        return data_dic
    else:
        log.error("获取数据长度不正确")
        return None


class ConMysql(object):
    def __init__(self):
        mysqlInfo = get_base_info()
        self.conn = pymysql.connect(**mysqlInfo)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.log = Log()

    # 删除表中所有数据
    def truncate_data(self, table):
        self.execute_sql("TRUNCATE TABLE {}".format(table))

    def execute_sql(self, sql):
        self.cursor.execute(sql)

    def query_one(self, sql):
        try:
            self.cursor.execute(sql)
            datas = self.cursor.fetchone()
        except Exception as e:
            self.log.error("sql语句错误---->{}".format(sql))
            return None
        return datas

    def query_all(self, sql):
        try:
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()
        except Exception as e:
            self.log.error("sql语句错误---->{}".format(sql))
            return None
        return datas

    def insert_data(self, table, **kwargs):
        sql = "INSERT INTO {} SET ".format(table)
        for key in kwargs.keys():
            if not key.__eq__("caseId"):
                if isinstance(kwargs[key], dict):
                    kwargs[key] = json.dumps(kwargs[key], ensure_ascii=False)
                elif isinstance(kwargs[key], str):
                    kwargs[key] = kwargs[key].replace("\'", "\"")
                elif isinstance(kwargs[key], int):
                    kwargs[key]=kwargs[key]
                elif kwargs[key].__eq__(""):
                    continue
                sql += "{}='{}',".format(key, kwargs[key])
        sql = sql[:-1]
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.log.error("sql语句错误---->{}".format(sql))

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    from common.handleCase import HandleCase

    # cases = HandleCase().get_cases()[0]
    con = ConMysql()
    # s = con.insert_data("testCase", **cases)


    res1 = con.query_all("select *  from apiInfo where apiId=1")
    res = con.query_all("select apiId from apiInfo where apiId=1")
    print(res)
    print(res1)

    # s={'caseId': 3, 'caseDescribe': '测试', 'apiHost': '/s5/login.mobile', 'params': '{"phone":"17711794059","code":"123456"}', 'method': 'post', 'relateApi': '', 'relateParams': '', 'expect': {'err_msg': '您的手机号'}}
    # for key in s.keys():
    #     print(type(s[key]))
