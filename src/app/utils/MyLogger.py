#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging import FileHandler, StreamHandler
import sys, os, logging

from app.utils.Singleton import Singleton


output_log_basepath = 'logs/rollBrick'
GCLogger = None

LOGGING_TYPE_FILE = 'FIRE'
LOGGING_TYPE_CONSOLE = 'CONSOLE'

LOG_FORMAT = "[%(asctime)s]: %(filename)s[line:%(lineno)d] [pid:%(process)d] %(levelname)s %(message)s"
class MyLoggerFactory(object):

    __metaclass__ = Singleton
    def __init__(self):
        self.logger_map = {}

    def getLogger(self, name, lever=logging.INFO, _type=LOGGING_TYPE_FILE):
        """ return logger"""
        if name not in self.logger_map:
            self.logger_map[name] = MyLogger(name, lever, _type)
        return self.logger_map[name]

class MyLogger():
    def __init__(self, name, lever=logging.INFO, _type=LOGGING_TYPE_FILE, saveToFile=False):
        if _type == LOGGING_TYPE_FILE:
            self.logger = self._getFileLogger(name, name, lever)
        else:
            self.logger = self._getConsoleLogger(name, lever, saveToFile)

    def debug(self, message):
        GCLogger.debug(message)
        self.logger.debug(message)

    def info(self, message):
        GCLogger.info(message)
        self.logger.info(message)

    def warning(self, message):
        GCLogger.warning(message)
        self.logger.warning(message)

    def error(self, message):
        GCLogger.error(message)
        self.logger.error(message)

    def _getConsoleLogger(self, name, lever, saveToFile):
        logger = logging.getLogger(name)

        self._setHandler(logger, StreamHandler)

        logger.setLevel(lever)

        if saveToFile:
            dir_path = self._mkdirByName(name)
            self._setHandler(logger, FileHandler, dir_path)
        return logger

    def _getFileLogger(self, logger_file, target_file, lever):
        logger = logging.getLogger(logger_file)
#         self._setHandler(logger, StreamHandler)

        dir_path = self._mkdirByName(logger_file)
        self._setHandler(logger, FileHandler, dir_path)
        logger.setLevel(lever)
        return logger

    def _setHandler(self, logger, handlerClass, *args, **kargs):
        handler = handlerClass(*args, **kargs)
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def _mkdirByName(self, name):
        dir_path = '%s%s' % (output_log_basepath, name)
        self._mkdir(dir_path)
        return '%s/%s.log' % (dir_path, name)

    def _mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            return False

    def get_this_exception_info(self):
        '''获取当前异常出现的信息
        输出: result={'type':exc_type,'value':exc_value,'tb':exc_tb,'line_number':exc_tb.lineno}
            type：异常类型  value：异常值    tb:异常信息   line_number:异常行数'''
        exc_type, exc_value, exc_tb = sys.exc_info()
        result = {}
        result['type'] = exc_type
        result['value'] = exc_value
        result['exc_tb'] = exc_tb
        result['line_number'] = exc_tb.tb_lineno
        return result

    def get_exception_lineno(self):
        '''取出异常行数
        '''
        return self.get_this_exception_info()['line_number']

GCLogger = MyLogger('GlobalConsoleLog', logging.DEBUG, LOGGING_TYPE_CONSOLE, True).logger
GFLogger = MyLoggerFactory().getLogger("GlobalLog", logging.ERROR)  # MyLoggerFactory().getLogger()


if __name__ == '__main__':
    GCLogger.error("haha")
