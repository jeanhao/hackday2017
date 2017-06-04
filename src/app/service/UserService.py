# -*- coding: utf-8 -*-
from flask.globals import session
from werkzeug.security import generate_password_hash, check_password_hash

from Configs import dbOper
from app.dbManager import DBTool  # @UnusedWildImport
from app.dbManager.DBModelFactory import DBModelFactory
from app.service.BaseService import BaseService
from app.utils.CommonUtils import *  # @UnusedWildImport
from app.utils.Singleton import Singleton


class UserService(BaseService):

    __metaclass__ = Singleton

    connectionWrapper = DBModelFactory().connectionWrapper
    def __init__(self):
        self.table = "tb_user"

    @connectionWrapper(dbOper.WRITE)
    def register(self, db_model, data):
        # 查询数据库是否已有数据
        sql = DBTool.select(self.table, ['id'], {'phone_num':data['phone_num']})
        res = db_model.GetOne(sql)
        if res:
            return pack(RetDefine.USER_NAME_USED)
        else:
            data['password'] = generate_password_hash(data['password'])
            sql = DBTool.insert(self.table, data)
            res = db_model.execute(sql)
            if not res.rowcount:
                return pack(RetDefine.SYS_ERR)
            data['id'] = res.lastrowid

            return pack()

    @connectionWrapper(dbOper.READ)
    def login(self, db_model_read, data):
        sql = DBTool.select(self.table, where={'phone_num':data['phone_num']})
        ret = db_model_read.GetOne(sql)
        if not ret:
            return pack(RetDefine.USER_NOT_EXIST)
        if not check_password_hash(ret['password'], (data['password'])):
            return pack(RetDefine.USERNAME_PASSWORD_NOT_MATCH)
        session['user'] = ret
        return pack()


    @connectionWrapper(dbOper.WRITE)
    def add_user(self, model, user):
        sql = DBTool.insert(self.table, user)
        model.execute(sql)

    @connectionWrapper(dbOper.WRITE)
    def dropUser(self, model, open_id):
        sql = DBTool.update(self.table, {'subscribe':0}, {'open_id':open_id})
        model.execute(sql)

