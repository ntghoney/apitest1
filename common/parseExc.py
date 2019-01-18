# -*- coding: utf-8 -*-
'''
@File  : parseExc.py
@Date  : 2019/1/15/015 17:50
'''
import xlrd
import os
from common.log import Log


class PaserExc(object):
    """
    sheetIndex:所解析exel表的索引
    """

    def __init__(self, path, sheetIndex):
        self.log = Log()
        if os.path.isfile(path):
            if os.path.exists(path):
                self.workbook = xlrd.open_workbook(path)
                self.sheet = self.workbook.sheet_by_index(sheetIndex)
                self.log.info("用例路径：{}".format(path))
            else:
                self.log.error("{}文件不存在".format(path))
        else:
            self.log.error("请检查{}路径是否正确".format(path))

    # 获得总行数
    def get_nrows(self):
        return self.sheet.nrows

    # 获得总列数
    def get_ncols(self):
        return self.sheet.ncols

    # 按行获得所有数据
    def get_row(self):
        rowValue = []
        for row in range(self.get_nrows()):
            rowValue.append(self.sheet.row_values(row))
        return rowValue


if __name__ == '__main__':
    pass
