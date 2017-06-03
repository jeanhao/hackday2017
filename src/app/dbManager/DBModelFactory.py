# -*- coding: utf-8 -*-

import copy
from functools import wraps
import random

from Configs import dbOper, dbConfigs
from app.dbManager.DBModel import DBModel
from app.utils.CommonUtils import pack
from app.utils.MyLogger import GCLogger
from app.utils.RetDefine import RetDefine
from app.utils.Singleton import Singleton


class DBModelFactory(object):

    __metaclass__ = Singleton
    def __init__(self):
        self.db_models_read = {}
        self.db_models = {}
        self.read_total_rate = 0
        self.write_total_rate = 0
        for dbConfig in dbConfigs:
            try:
                self.createDBModel(dbConfig)
            except Exception:
                GCLogger.error("can't connect to %s" % dbConfig['name'])

    def makeModel(self, dbConfig, readonly):
        return  {'config':dbConfig, 'db':DBModel(copy.copy(dbConfig), readonly)}

    # @dbConfigs
    #   name : 数据模型名字，用于区分多个数据库的连接
    #   host : 数据库写地址
    #   user : 数据库用户名
    #   passwd : 数据库密码
    #   db_name : 数据库名称
    #   port : 数据库端口，默认为3306
    #   charset : 数据库字体集，默认为utf8
    #   cursorclass : 取数据时游标类型，默认为pymysql.cursors.DictCursor（可以自动转为Key-Value的结果集）
    def createDBModel(self, dbConfig):
        db_name = dbConfig['name']
        db_type = dbConfig['db_type']
        db_rate = dbConfig['rate']
        if not self.db_models.has_key(db_name):
            if db_type == dbOper.READ:
                self.read_total_rate += db_rate
                self.db_models_read[db_name] = self.makeModel(dbConfig, True)
            elif db_type == dbOper.WRITE:
                self.write_total_rate += db_rate
                self.db_models[db_name] = self.makeModel(dbConfig, False)
            else:
                self.read_total_rate += db_rate
                self.db_models_read[db_name] = self.makeModel(dbConfig, True)
                self.write_total_rate += db_rate
                self.db_models[db_name] = self.makeModel(dbConfig, False)

    # name : 数据模型名字，用于区分多个数据库的连接
    # readonly : 用来标识要是获取可读写还是只读的数据模型
    def getDBModel(self, oper=dbOper.READ, name=None):
        if name:
            return self.db_models.get(name, self.db_models_read.get(name))
        else:
            if oper == dbOper.READ:
                return self.chooseModels(), None
            elif oper == dbOper.WRITE:
                return None, self.chooseModels(False)
            return self.chooseModels(), self.chooseModels(False)

    def chooseModels(self, readonly=True):
        total_rate = readonly and self.read_total_rate or self.write_total_rate
        num = random.randint(0, total_rate)
        tmp_total = 0
        models = readonly and self.db_models_read or self.db_models
        for model in models.values():
            tmp_total += model['config']['rate']
            if num <= tmp_total:
                return model['db']

        return None

    @staticmethod
    def initModel(db_model):
        conn = db_model.connect()
        db_model.local.cursor = conn.cursor()
        return db_model

    # 事务装饰器
    def connectionWrapper(self, oper=dbOper.READ):
        def real_decorator(func):
            @wraps(func)
            def lazy_func(obj, *args, **kargs):
                if args and isinstance(args[0], DBModel):
                    return func(obj, *args, **kargs)
                ret_val = -1
                try:
                    db_model_read, db_model = self.getDBModel(oper)
                    if oper == dbOper.READ:
                        ret_val = func(obj, self.initModel(db_model_read), *args, **kargs)
                    elif oper == dbOper.WRITE:
                        ret_val = func(obj, self.initModel(db_model), *args, **kargs)
                        db_model.local.conn.commit()
                    else:
                        ret_val = func(obj, self.initModel(db_model_read), self.initModel(db_model), *args, **kargs)
                        db_model.local.conn.commit()
                except Exception, e:
                    GCLogger.error(e)
                    if oper != dbOper.READ:
                        db_model.local.conn.rollback()
                    return pack(RetDefine.SYS_ERR)
                return ret_val
            return lazy_func
        return real_decorator
