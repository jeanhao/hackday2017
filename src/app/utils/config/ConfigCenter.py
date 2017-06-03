#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Configs import dbOper
from app.dbManager import DBTool
from app.dbManager.DBModelFactory import DBModelFactory
from app.utils.MyLogger import MyLoggerFactory
from app.utils.RetDefine import RetDefine
from app.utils.Singleton import Singleton
from app.utils.config.Configer import Configer


class ConfigCenter(object):
    
    __metaclass__ = Singleton
    
    logger = MyLoggerFactory().getLogger(__name__)
    connectionWrapper = DBModelFactory().connectionWrapper
    
    def __init__(self, conf_file=None):
        
        self.configTable = 'tb_config'

        retAllConifgs = self._loadConfig()
        if retAllConifgs != RetDefine.SYS_ERR:
            self._rawConfigs = retAllConifgs
        else:
            self._rawConfigs = []
        self._configs = {}
        for config in self._rawConfigs:
            self._configs[config['file']] = Configer(config)
    
    def getConfig(self, *args):
        ret = self._configs
        for arg in args:
            if self._configs.get(arg):
                ret = self._configs[arg]
        return ret
    
    @connectionWrapper(dbOper.WRITE)
    def deleteConfigByName(self, dbModel, data):
        try:
            sql = DBTool.delete(self.configTable, data)
            ret_del = self.db_model.execute(sql)
            if ret_del.rowcount:
                return RetDefine.NO_ERR
        except Exception, e:
            self.logger.error("ConfigCenter delete_config error. sql=[%s],msg=[%s]" % (repr(sql), repr(e)))
        return RetDefine.SYS_ERR
    
    @connectionWrapper(dbOper.WRITE)
    def updateConfig(self, dbModel, data):
        try:
            sql = DBTool.update(self.configTable, {"value":"%s", "type":"%s"}, {"name":"%s"})
            if type(data) == list:
                ret = dbModel.executemany(sql, data)
            else:
                ret = dbModel.execute(sql)
            if ret.rowcount:
                return RetDefine.NO_ERR
        except Exception, e:
            self.logger.error("ConfigCenter update_confg error. sql=[%s],msg=[%s]" % (repr(sql), repr(e)))
        return RetDefine.SYS_ERR
    
    @connectionWrapper(dbOper.WRITE)
    def addConfig(self, dbModel, data):
        try:
            sql = DBTool.insert(self.configTable, data)
            ret = self.db_model.execute(sql)
            if ret.rowcount:
                return RetDefine.NO_ERR
        except Exception, e:
            self.logger.error("ConfigCenter addConfig error. sql=[%s],msg=[%s]" % (repr(sql), repr(e)))
        return RetDefine.SYS_ERR

    @connectionWrapper()
    def _loadConfig(self, dbModel_read, where=None):
        try:
            sql = DBTool.select(self.configTable, where=where)
            configs = dbModel_read.GetList(sql)
            if configs:
                return configs
        except Exception, e:
            self.logger.error("ConfigCenter getConfigs error. sql=[%s],msg=[%s]" % (repr(sql), repr(e)))
        return RetDefine.SYS_ERR
