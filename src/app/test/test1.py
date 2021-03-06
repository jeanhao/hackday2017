#!/usr/bin/env python
# encoding: utf-8

import json
import urllib
import urllib2
import cookielib

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

def send_req(url, data=None):
    url = "%s%s" % (base_url, url)
    if data:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    ret = opener.open(req)
    return ret.read()

def json_req(url, data=None):
    url = "%s%s" % (base_url, url)
    if data:
        data = json.dumps(data)  # 对数据进行JSON格式化编码
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(url, headers=headers, data=data)  # 生成页面请求的完整数据
    response = opener.open(req)  # 发送页面请求
    return response.read()

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

base_url = 'http://127.0.0.1:5000/api/'

if __name__ == '__main__':
    phone_num = '15629071220'
#     print json_req('user/message', {'phone_num':phone_num})
#     code = raw_input('input code')
#     print send_req('user/register', {'phone_num':phone_num, 'nickname':'zenghao', 'verify_code':code, 'password':"123"})
#     print json_req('user/login', {'phone_num':'15629071220', 'password':"qwe123"})
#     print json_req('plant/list')
#     print json_req('plant/add', {"pt_type":'type1', "age":10, "nickname":"tree"})
#     print json_req('task/answer/confirm', {u'week_size': 3, u'has_weekend': 1, u'answers': [{'ans_type':1,
# "begin_time":"",
# "bottom_times":0,
# "content":"制定一个未来2天的计划，编辑自定义任务5个",
# "end_time":"",
# "id":312,
# "problem_id":2,
# "top_times":5}]})
    print json_req('task/answer/list')
#     print json_req('pl nt/detail/2')

