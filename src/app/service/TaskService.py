# -*- coding: utf-8 -*-
from flask.globals import session

from Configs import dbOper
from app.dbManager import DBTool  # @UnusedWildImport
from app.dbManager.DBModelFactory import DBModelFactory
from app.service.BaseService import BaseService
from app.utils.CommonUtils import *  # @UnusedWildImport
from app.utils.Singleton import Singleton
from app.utils.mp.MpManager import MpManager

TIME_FORMAT_MINI = '%Y-%m-%d %H:%M'

NOTICE_CONTENT = """亲爱的%s，你的“告别拖延”养成计划已生成！
从今天开始，未来三周内。
每天我都会提醒你去完成当日任务。（每周有一次修改任务机会）
并不定期用禁令来拷问你的良心，
虽然不一定会痛。

总之，任务卡没有完成或者违反禁令，
都会得到令人失落的反馈，
所以，请一定要加油哦。"""
class TaskService(BaseService):

    __metaclass__ = Singleton

    connectionWrapper = DBModelFactory().connectionWrapper
    def __init__(self):
        self.tag_table = "tb_tag"
        self.problem_table = "tb_problem"
        self.tp_table = "tb_tag_problem"
        self.answer_table = "tb_answer"
        self.up_table = "tb_user_problem"
        self.user_table = "tb_user"

    @connectionWrapper(dbOper.READ)
    def list_tag(self, model):
        sql = DBTool.select(self.tag_table)
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.READ)
    def list_problem(self, model, tags):
        sql = "select distinct p.id,p.content from tb_problem as p left join tb_tag_problem as tp on tp.problem_id = p.id where tp.tag_id in (%s)" % tags
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.READ)
    def answer_problem(self, model, problems):

        # 2 添加新的
#         for problem in problems:
#             data = {"problem_id":problem, "open_id":open_id}
#             sql = DBTool.insert(self.up_table, data)
#             model.execute(sql)
        # 获取新的问题
        sql = DBTool.select(self.answer_table, where={("problem_id", "in"):problems})
        res = model.GetList(sql)
        return pack(data=res)

    @connectionWrapper(dbOper.WRITE)
    def comfirm_answer(self, model, data):
        # 更新用户问题列表
        # 1 删除旧的
        open_id = session['user']['open_id']
        where = {"open_id":open_id}
        sql = DBTool.delete(self.up_table, where)
        model.execute(sql)
        # 2 更新用户数据
        sql = DBTool.update(self.user_table, data, where, ['has_weekend', 'week_size'])
        model.execute(sql)
        # 插入新的任务数据
        for answer in data['answers']:
            answer['open_id'] = open_id
            if 'id' in answer:
                answer.pop('id')
#                 sql = DBTool.select(self.answer_table, ['content'], {'id':answer['id']})
#                 res = model.GetOne(sql)
#                 answer['answer_content'] = res['content']
            sql = DBTool.insert(self.up_table, answer)
            print sql
            model.execute(sql)
        MpManager().sendMsg(open_id, 'text', NOTICE_CONTENT)
        return pack()

    @connectionWrapper(dbOper.READ)
    def list_answer(self, model):
        open_id = session['user']['open_id']
        where = {"open_id":open_id}
        sql = DBTool.select(self.user_table, ['has_weekend', 'week_size'] , where)
        data = model.GetOne(sql)
        if not data:
            return pack(RetDefine.SYS_ERR)
        sql = DBTool.select(self.up_table, where=where)
        problems = model.GetList(sql)
        data['problems'] = problems
        return pack(data=data)

    @connectionWrapper(dbOper.READ)
    def get_tasks(self, model):
        sql = DBTool.select(self.up_table, {'ans_type':0})
        tasks = model.GetList(sql)
        now = time.time()
        ret_task = {}
        for task in tasks:
            date_str = "%s %s" % get_now_time(), task['begin_time']
            t = time.mktime(time.strptime(date_str, TIME_FORMAT_MINI))
            if t < now:  # 跳过已过去的
                continue
            if t not in ret_task:
                ret_task[t] = [task]
            else:
                ret_task[t].append(task)
        return ret_task

    @connectionWrapper(dbOper.WRITE)
    def add_tag(self, model):
        tags = """拖延症
死肥宅
不运动
碳酸饮料狂
爱吃油炸食品鸡
吸一点点
泡面承包户
又咸鱼又丧
熬夜党
手机依赖症
剁手党""".split("\n")
        for tag in tags:
            sql = DBTool.insert(self.tag_table, {"tag_name":tag})
            model.execute(sql)

    @connectionWrapper(dbOper.WRITE)
    def add_problem(self, model):
        for i in xrange(100):
            for j in xrange(3):
                data = {"content":'answer%d' % i, 'problem_id':i, 'choice':j}
                sql = DBTool.insert(self.answer_table, data)
                model.execute(sql)

    @connectionWrapper(dbOper.WRITE)
    def add_test(self, model):
        for i in xrange(100):
            for j in xrange(47, 57):
                data = { 'problem_id':i, 'tag_id':j}
                sql = DBTool.insert(self.tp_table, data)
                model.execute(sql)

if __name__ == '__main__':
    TaskService().add_test()
