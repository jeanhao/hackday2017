# -*- coding: utf-8 -*-
from flask.globals import session

from Configs import dbOper
from app.dbManager import DBTool  # @UnusedWildImport
from app.dbManager.DBModelFactory import DBModelFactory
from app.service.BaseService import BaseService
from app.utils.CommonUtils import *  # @UnusedWildImport
from app.utils.Singleton import Singleton


class PlantService(BaseService):

    __metaclass__ = Singleton

    connectionWrapper = DBModelFactory().connectionWrapper
    def __init__(self):
        self.table = "tb_plant_record"

    @connectionWrapper(dbOper.READ)
    def list_plant(self, db_model):
        # 查询数据库是否已有数据
        sql = DBTool.select(self.table, ['id', 'nickname'], where={'user_id':session['user']['id']})
        res = db_model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.WRITE)
    def detail_plant(self, db_model, _id):
        # 查询数据库是否已有数据
        sql = DBTool.select(self.table, where={'id':_id})
        res = db_model.GetOne(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.WRITE)
    def add_plant(self, db_model, data):
        data['create_date'] = get_now_time()
        data['user_id'] = session['user']['id']
        sql = DBTool.insert(self.table, data)
        res = db_model.execute(sql)
        if not res.rowcount:
            return pack(RetDefine.SYS_ERR)
        else:
            return pack()

    @connectionWrapper(dbOper.WRITE)
    def del_plant(self, db_model, data):
        data['user_id'] = session['user']['id']
        sql = DBTool.delete(self.table, data)
        res = db_model.execute(sql)
        if not res.rowcount:
            return pack(RetDefine.SYS_ERR)
        else:
            return pack()
