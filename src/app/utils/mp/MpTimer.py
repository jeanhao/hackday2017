#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年4月29日

@author: zenghao
'''
from app.utils.Singleton import singleton
from app.utils.RedisClient import RedisClient
from app.utils.CommonUtils import send_req, filterMap, send_json, get_now_date
from app.service.UserService import UserService
from app.service.TaskService import TaskService
from collections import OrderedDict
from threading import Thread
import time
from app.utils.mp.MpManager import MpManager

class MpTimer(Thread):
    """
    公众号定时发送任务模块
    """
    def __init__(self):
        Thread.__init__(self, name="mp_timer")
        self.redisClient = RedisClient()
        self.tasks = self.get_tasks()

    def get_tasks(self):
        tasks = TaskService().get_tasks()
        if tasks:
            return OrderedDict(tasks)

    def run(self):
        while True:
            for timestamp, task in self.tasks.items():
                if timestamp > time.time():
                    time.sleep(timestamp - time.time())
                open_id = task['open_id']
                content = "你的任务【%s】开始时间到啦~" % task.get('answer_content')
                MpManager().sendMsg(open_id, 'text', content)

# if __name__ == '__main__':
#     users = MpTimer().getUserList(detail=True)
#     for open_id, info in users.items():
#         data = {"open_id":open_id, "create_date":get_now_date(), "nickname":info['nickname'], 'gender':info['sex']}
#         UserService().add_user(data)
