# -*- coding: utf-8 -*-
from flask.globals import session

from Configs import dbOper
from app.dbManager import DBTool  # @UnusedWildImport
from app.dbManager.DBModelFactory import DBModelFactory
from app.service.BaseService import BaseService
from app.utils.CommonUtils import *  # @UnusedWildImport
from app.utils.Singleton import Singleton


class TaskService(BaseService):

    __metaclass__ = Singleton

    connectionWrapper = DBModelFactory().connectionWrapper
    def __init__(self):
        self.tag_table = "tb_tag"
        self.problem_table = "tb_problem"
        self.tp_table = "tb_tag_problem"
        self.answer_table = "tb_answer"
        self.up_table = "tb_user_problem"

    @connectionWrapper(dbOper.READ)
    def list_tag(self, model):
        sql = DBTool.select(self.tag_table)
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.READ)
    def list_problem(self, model, tags):
        tags_str = ", ".join(tags)
        sql = "select distinct p.id,p.content from tb_problem as p left join tb_tag_problem as tp on tp.problem_id = p.id where tp.tag in %s" % tags_str
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.WRITE)
    def answer_problem(self, model, problems):
        # 更新用户问题列表
        # 1 删除旧的
        open_id = session['user']['open_id']
        sql = DBTool.delete(self.up_table, {"open_id":open_id})
        model.execute(sql)
        # 2 添加新的
        for problem in problems:
            data = {"problem_id":problem, "open_id":open_id}
            sql = DBTool.insert(self.up_table, data)
            model.execute(sql)
        # 获取新的问题
        sql = DBTool.select(self.answer_table, where={("problem_id", "in"):problems})
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.WRITE)
    def add_tag(self, model):
        tags = "拖延症/邋遢/宅男/学渣/游戏迷/肥胖/不爱运动/追剧迷/挂科户/碳酸饮料狂/爱吃鸡排/吸一点点/泡面承包户/不运动/咸鱼/废柴/丧/宅/氪金/熬夜党/赖床党/手机依赖症/剁手党".split("/")
        for tag in tags:
            sql = DBTool.insert(self.tag_table, {"tag_name":tag})
            model.execute(sql)

if __name__ == '__main__':
    TaskService().add_tag()
