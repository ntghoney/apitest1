# -*- coding: utf-8 -*-
'''
@File  : log.py
@Date  : 2019/1/15/015 17:35
'''
import logging
from common.parseConfig import setPath
import datetime



def get_now():
    return datetime.datetime.now()


class Log(object):

    def __init__(self):
        filename = "{}.log".format(get_now().strftime("%Y%m%d"))
        self.logPath = setPath(pathName="log", fileName=filename)
        self.log = logging.getLogger(__name__)
        self.log.setLevel(level=logging.INFO)
        # 配置日志输出文件
        self.handler = logging.FileHandler(self.logPath)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        # 配置日志输出控制台
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        self.console.setFormatter(self.formatter)
        # 使日志输出到控制台和日志文件
        self.log.addHandler(self.handler)
        self.log.addHandler(self.console)

    def info(self, msg):
        return self.log.info(msg)

    def error(self, msg):
        return self.log.info(msg)

    def debug(self, msg):
        return self.log.debug(msg)


if __name__ == '__main__':
    log = Log()
    log.info("hello")
