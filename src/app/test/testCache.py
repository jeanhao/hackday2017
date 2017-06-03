#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年4月27日

@author: zenghao
'''
from app.service.TaskService import TaskService
from app.dbManager.DBModelFactory import DBModelFactory
from app.utils.CommonUtils import get_now_date, get_now_time, check_time
from app.dbManager.DBConfigs import db_oper
from app.dbManager import DBTool
from app.utils.Singleton import singleton
import random
from functools import wraps
import time
from app.utils.cache.LocalCache import CacheFactory

def check_time(func):
    @wraps(func)
    def lazy_fun(*args, **kargs):
        start = time.clock()
        ret = func(*args, **kargs)
        end = time.clock()
        print(func.__name__ + " api cost time %f s" % (end - start))
        return ret
    return lazy_fun

@singleton
class TestCache():

    connection_wrapper = DBModelFactory().connection_wrapper

    def __init__(self, testTable="t_bbm_task"):
        self.table = testTable
        self.cache = CacheFactory().getCache("test")

    @connection_wrapper(db_oper.WRITE)
    def addfortest(self, dbModel):
        for i in xrange(100000):
            dbModel.execute(DBTool.sql_insert(self.table, self.makeRecord(i)))

    def makeRecord(self, i):
        return {
            "title":"title%d" % i,
            "detail":"detail%d" % i,
            "money":i,
            "end_date":"end_date%d" % i,
            "pub_user":"pub_user%d" % i,
            "create_date":get_now_time(),
            "pub_wxid":"pub_wxid%d" % i
            }


    @connection_wrapper(db_oper.READ)
    @check_time
    def getDataByDB(self, dbModel):
        for i in range(1, 5000):
            i %= 100
#         for i in random.sample(range(1, 100), 5000):
            sql = DBTool.sql_select(self.table, where={"task_id":i})
            data = dbModel.GetOne(sql)
            print data

    @connection_wrapper(db_oper.READ)
    @check_time
    def getDataByDBWithCache(self, dbModel):
        for i in range(1, 5000):
#         for i in random.sample(range(1, 100), 5000):
            i %= 100
            data = self.cache.get(i)
            if not data:
                sql = DBTool.sql_select(self.table, where={"task_id":i})
                data = dbModel.GetOne(sql)
                self.cache.set(i, data)
            print data

    @check_time
    def test(self, d):
        for _ in xrange(10000000):
            pass

if __name__ == '__main__':
#     TestCache().addfortest()
    d = {}
    for i in xrange(100000):
        d[i] = "ttt"

    TestCache().test(d)
