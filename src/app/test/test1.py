#!/usr/bin/env python
# encoding: utf-8

import json
import urllib
import urllib2


def send_req(url, data=None):
    url = "%s%s" % (base_url, url)
    if data:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    ret = urllib2.urlopen(req)
    return ret.read()

def send_json(info, userid=None):
    url = "http://www.tuling123.com/openapi/api"
    APIKEY = "1e4b631f8d274edab438c3bbd8cfe5fc"
    if type(info) != str:
        info = info.encode('u8')
#     values = {"keserid“”：’ userid
    jdata = urllib.urlencode(values)  # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
    response = urllib2.urlopen(req)  # 发送页面请求
    return response.read()

base_url = 'http://127.0.0.1:5000/'

if __name__ == '__main__':
#     print send_json(u"你爸爸是谁")
#     data = {'title':'test','detail':'detail12313','money':123,'end_date':'12312432'}
#     print send_req('task/add', data)
    print send_req('user/message', {'phone_num':'15629071220', 'nickname':'zenghao'})
#     print send_req('task/detail?task_id=7')
#     print send_req('task/cancel',{'task_id':'7'})
#     print send_req('task/accepted',{'task_id':'7'})

