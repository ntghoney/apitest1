# -*- coding: utf-8 -*-
'''
@File  : report.py
@Date  : 2019/1/16/016 9:45
'''
from common.log import Log, get_now
import xlwt
from xlwt import *
from common.parseConfig import setPath
from common.parseConfig import ParseConfig


class Report(object):
    def __init__(self):
        self.log = Log()
        self.__result_info = None
        reportInfo = ParseConfig().get_info("report")
        self.reportNcols = int(reportInfo["ncols"])  # 总列数
        self.reportTitle = reportInfo["title"]  # 报告标题
        self.reportColName = str(reportInfo["colname"]).split(",")  # 报告列名
        self.reportPath = setPath(pathName="report", fileName="{}接口自动化测试报告.xls".format(get_now().strftime("%Y%m%d")))
        # 新建excel
        self.workbook = xlwt.Workbook()

        self.table = self.workbook.add_sheet(u"接口测试报告", cell_overwrite_ok=True)

    # 设置列宽
    def set_col_width(self, ncols, width):
        for i in range(ncols):
            self.table.col(i).width = width

    # 设置垂直居中
    def set_center(self):
        alignment = xlwt.Alignment()  # 设置居中
        # alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        return alignment

    # 设置垂直水平居中
    def set_all_center(self):
        alignment = xlwt.Alignment()  # 设置居中
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        return alignment

    # 设置自动换行
    def auto_line(self):
        alignment = xlwt.Alignment()
        alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        return alignment

    # 标题样式
    def title_style(self):
        style = xlwt.easyxf('pattern: pattern solid, fore_colour 0x16;')  # 设置背景颜色为灰色
        style.alignment = self.set_all_center()
        style.font.height = 800
        style.font.bold = True  # 设置加粗
        return style

    # 列名单元格样式
    def col_name_style(self):
        style = xlwt.easyxf('pattern: pattern solid, fore_colour 0x16;')
        style.font.height = 400
        style.alignment = self.set_center()
        return style

    # 自动换行样式
    def col_auto_line_style(self):
        style = XFStyle()
        style.font.height = 250
        style.alignment = self.set_center()
        return style

    # 自动换行，垂直居中
    def style1(self):
        style = XFStyle()
        style.font.height = 250
        style.alignment = self.auto_line()
        style.alignment.vert = xlwt.Alignment.VERT_CENTER
        return style

    def result_info_style(self):
        style = XFStyle()
        font = xlwt.Font()
        font.name = "宋体"
        font.height = 500
        style.font = font
        return style

    # 普通单元个样式
    def col_style(self):
        style = XFStyle()
        style.alignment = self.set_center()
        style.font.height = 250
        return style

    def write(self, row, col, msg="", style=Style.default_style):
        self.table.write(row, col, msg, style)

    def write_merge(self, r1, r2, c1, c2, msg="", style=Style.default_style):
        self.table.write_merge(r1, r2, c1, c2, msg, style)

    def set_result_info(self, result_info):
        self.__result_info = result_info

    # 逐行写入数据
    def write_line(self, row, resdic):
        for key in resdic.keys():
            if key.__eq__("caseId"):
                self.write(row, 0, resdic[key], self.style1())
            elif key.__eq__("caseDescribe"):
                self.write(row, 1, resdic[key], self.style1())
            elif key.__eq__("apiHost"):
                self.write(row, 2, resdic[key], self.style1())
            elif key.__eq__("except"):
                self.write(row, 4, resdic[key], self.style1())
            elif key.__eq__("apiParams"):
                self.write(row, 3, resdic[key], self.style1())
            elif key.__eq__("fact"):
                self.write(row, 5, resdic[key], self.col_style())
            elif key.__eq__("databaseResult"):
                self.write(row, 6, resdic[key], self.col_style())
            elif key.__eq__("databaseExpect"):
                self.write(row, 7, resdic[key], self.col_style())
            elif key.__eq__("ispass"):
                self.write(row, 8, resdic[key], self.col_style())
            elif key.__eq__("time"):
                self.write(row, 9, resdic[key], self.style1())
            elif key.__eq__("reason"):
                self.write(row, 10, resdic[key], self.style1())

    def get_report(self, result):
        global row, ncols
        ncols = self.reportNcols
        row = 3  # 从第二行写入用例执行情况
        # 设置测试报告列宽
        self.set_col_width(ncols, 6000)
        # 标题内容
        self.write_merge(0, 0, 0, ncols - 1, self.reportTitle, self.title_style())
        # 写入列名，逐列写入
        for col in range(self.reportNcols):
            self.write(2, col, self.reportColName[col], self.col_name_style())
        # 写入用例执行统计情况
        self.write_merge(1, 1, 0, ncols - 1, self.__result_info, self.result_info_style())
        # 写如用例执行情况
        self.log.info("正在写入用例执行情况")
        for res in result:
            self.write_line(row, res)
            row += 1
        self.workbook.save(self.reportPath)


if __name__ == '__main__':
    # import xlwt
    # from datetime import datetime
    # from xlwt import *  # 引入相应的库
    #
    # style0 = xlwt.easyxf('font: name Times New Roman',
    #                      num_format_str='#,##0.00', )  # 字体的颜色
    # styleOK = easyxf('pattern: fore_colour light_blue;'
    #                  'font: colour green, bold True;')
    # alignment = xlwt.Alignment()  # 设置居中
    # alignment.horz = xlwt.Alignment.HORZ_CENTER
    # alignment.vert = xlwt.Alignment.VERT_CENTER
    # style0.font.height = 280
    # style3 = XFStyle()
    # style3.alignment = alignment  # 给样式添加文字居中属性
    # style3.font.height = 330  # 设置字体大小
    # pattern = xlwt.Pattern()  # 一个实例化的样式类
    # pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 固定的样式
    # pattern.pattern_fore_colour = xlwt.Style.colour_map['red']  # 背景颜色
    # styleOK.pattern = pattern
    # style1 = xlwt.easyxf(num_format_str='DD-MM-YY')  # 显示时间定义时间的样式
    # wb = xlwt.Workbook()
    # ws = wb.add_sheet('测试用')
    # for i in range(6):  # 定义列宽
    #     ws.col(i).width = 200 * 30
    # ws.write_merge(0, 0, 0, 5, '测试报告', style3)
    # ws.write(1, 0, '测试时间', style0)
    # ws.write(1, 1, datetime.now(), style1)
    # ws.write(1, 2, '测试人', style0)
    # ws.write(1, 3, '雷子', styleOK)
    # wb.save('res.xls')
    res = [{"id": 1, "name": "a", "host": "192.168.0.1", "exc": "a", "fact": "fact", "ispass": "pass",
            "time": "2018/12/1"},
           {"id": 1, "name": "a", "host": "192.168.0.1", "exc": "a", "fact": "fact", "ispass": "pass",
            "time": "2018/12/1"},
           {"id": 1, "name": "a", "host": "192.168.0.1", "exc": "a", "fact": "fact", "ispass": "pass",
            "time": "2018/12/1"},
           {'id': 1, 'name': '测试', 'host': '/s5/login.mobile',
            'except': "{'err_code': '10001', 'err_msg': '您的手机号未绑定钱咖帐号'}",
            'fact': '{\n  "err_code": 10001,\n  "err_msg": "您的手机号未绑定钱咖帐号",\n  "messages": [],\n  "payload": {}\n}',
            'ispass': 'fail', 'time': '2019/01/17 15:26:45', 'reason': '网络连接错误或其他错误，接口返回200'}]
    r = Report()
    r.get_report(res)
