#!/usr/bin/python2.7
# encoding: utf-8

'''
Created on 2017年4月29日

@author: zenghao
'''
from app.utils.Singleton import singleton
from app.utils.RedisClient import RedisClient
from configs import Config
from time import sleep
from app.utils.CommonUtils import send_req, filterMap, send_json
import json
from app.service.UserService import UserService
import time

@singleton
class MpManager(object):

    def __init__(self):
        self.redisClient = RedisClient()

    def getToken(self, check_valid=True):
        """"
        @note: 获取token，先从缓存中取
        """
        token = self.redisClient.get(Config.MP_TOKEN)
        if not token:  # 不存在，重新获取
            while not self.redisClient.lock(Config.MP_TOKEN_LOCK):  # 拿不到锁
                sleep(0.1)
                token = self.redisClient.get(Config.MP_TOKEN)
                if token:
                    break
            else:
                try:
                    # 获取微信token
                    res = send_req(Config.ACCESS_TOKEN_URL)
                    token_data = json.loads(res)
                    token = token_data['access_token']
                    self.redisClient.set(Config.MP_TOKEN, token, ex=token_data['expires_in'] - 100)
                finally:
                    self.redisClient.unlock(Config.MP_TOKEN_LOCK)
        return token

    def getUserList(self, nextOpenId=None, detail=False):
        """
        @note: 获取用户列表，通过detail参数控制是否获取详情信息
        """
        token = self.getToken()
        url = Config.USER_LIST_URL % token
        if nextOpenId:
            url = "%s&next_openid=%s" % (url, nextOpenId)
        res = send_req(url)
        data = json.loads(res)
        openids = data['data']['openid']
        if not detail:
            return openids
        else:
            userinfos = {}
            for openid in openids:
                res = self.getDetailUser(openid, token)
                if res.get('subscribe', 0):  # 已关注公众号
                    userinfos[openid] = res
            return userinfos

    def getDetailUser(self, openid, token=None):
        """
        @note: 获取用户详情
        """
        if not token:
            token = self.getToken()
        res = send_req(Config.USER_DETAIL_URL % (self.getToken(), openid))
        return json.loads(res)

    def sendMsg(self, touser, msgtype, detail, token=None):
        """
        @note: 给用户发送消息
        """
        data = {
            "touser":touser,
            "msgtype":msgtype,
            msgtype:detail,
        }
        token = token if token else self.getToken()
        res = send_json(Config.SEND_MSG_URL % token , data)
        return res

    def sendTemplate(self, touser, template_id, data, url="", topcolor='"#FF0000"', token=None):
        data = {
            "touser":touser,
            "template_id":template_id,
            "url":url,
            "topcolor":"#FF0000",
            "data":data
        }
        token = token if token else self.getToken()
        res = send_json(Config.TEMPLATE_SEND_URL % token , data)
        return res
if __name__ == '__main__':
    touser = "o-UJCxIpgmE8Mq_KaYaJXdoOsWWw"
    template_id = Config.TEMPLATE_ID_1
    url = "www.baidu.com"
    data = {
        "first": {
           "value":"有人接单啦",
           "color":"#173177"
       },
       "keyword1":{
           "value":"卖巧克力",
           "color":"#173177"
       },
       "keyword2": {
           "value":"111",
           "color":"#173177"
       },
       "keyword3": {
           "value":"9999",
           "color":"#173177"
       },
        "keyword4": {
           "value":"2014年9月22日",
           "color":"#173177"
       },
       "remark":{
           "value":"欢迎再次购买！",
           "color":"#173177"
       }
    }
    MpManager().sendTemplate(touser, template_id, data, url)
