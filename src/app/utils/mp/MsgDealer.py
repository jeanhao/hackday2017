#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年4月29日

@author: zenghao
'''
from app.utils.MyLogger import GFLogger
import traceback
from flask.helpers import make_response
import time
from app.utils.Singleton import singleton
from app.service.UserService import UserService
from app.utils.RedisClient import RedisClient
from app.utils.mp.MpManager import MpManager
from app.utils.CommonUtils import filterMap, get_now_date

CONTENT_KEYWORDS = {
"计划开始":
"""亲爱的石楠，你的“告别拖延”养成计划以生成，
从今天开始，未来三周内，
每天我都会提醒你去完成当日任务，
并不定期用禁令来拷问你的良心，
虽然不一定会痛。
总之，任务卡没有完成或者违反禁令，
都会得到令人失落的反馈，
所以，请一定要加油哦。

回复【任务卡】领取任务。""",

"任务卡":
"""
“告别拖延”养成计划第一天

今日任务：
时间性任务1      验证码【060401】
时间性任务1      验证码【060402】
。。。。。。

本周禁令
吃油炸食品    不超过   2次
喝碳酸饮料    不超过   2次
给父母电话    不低于   1次
。。。
任务完成后，请务必记得回复验证码完成打卡，
否则我会自动判断为“你在偷懒”哟。

060401
时间性任务1       打卡完成！
今日已打卡：
时间性任务1

今日未打卡：
时间性任务2      验证码【060402】


如果你觉得动力不足，
可以回复【鸡汤】
我有惊喜给你！
"""

}
@singleton
class MsgDealer(object):

    def __init__(self):
        self.userService = UserService()
        self.redisClient = RedisClient()
        self.mpManager = MpManager()

    def deal(self, data):
        try:
            print data
            method = getattr(self, data['MsgType'])
            res = method(data)
            if not res:
                return ""
            else:
                resp = make_response(res)
                resp.content_type = 'application/xml'
                return resp
        except Exception as e:
            GFLogger.error(traceback.format_exc(e))
            return ""

    def text(self, data):
        return self.dealContent(data)

    def dealContent(self, data):
        content = data['Content']
        for keyword in CONTENT_KEYWORDS:
            if keyword == content:
                content = CONTENT_KEYWORDS[keyword]
                break
        return self.respText(data['FromUserName'], data['ToUserName'], content)

    def event(self, data):
        event = data['Event']
        if event == "subscribe":  # 用户关注微信号
            GFLogger.debug("subscribe event happend")
            userinfo = self.mpManager.getDetailUser(data['FromUserName'])
            user = {"open_id":userinfo['open_id'], "create_date":get_now_date(), "nickname":userinfo['nickname'], 'gender':userinfo['sex']}
            self.userService.addUser(user)
            return self.respText(data['FromUserName'], data['ToUserName'], "欢迎关注公众号")
        elif event == "unsubscribe":  # 用户取消关注微信号
            GFLogger.debug("unsubscribe event happend")
            self.userService.dropUser(data['FromUserName'])

    def image(self, data):
        pass

    def voice(self, data):
        pass

    def video(self, data):
        pass

    def shortvideo(self, data):
        pass

    def location(self, data):
        pass

    def link(self, data):
        pass

    def respText(self, toUser, fromUser, content):
        return "<xml>\
<ToUserName><![CDATA[%s]]></ToUserName>\
<FromUserName><![CDATA[%s]]></FromUserName>\
<CreateTime>%s</CreateTime>\
<MsgType><![CDATA[text]]></MsgType>\
<Content><![CDATA[%s]]></Content>\
</xml>" % (toUser, fromUser, str(int(time.time())), content)

