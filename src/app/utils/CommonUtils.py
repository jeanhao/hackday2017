# coding=UTF-8

from _functools import partial
import datetime
from functools import wraps
import json, random, string, urllib, urllib2
import time

from flask import session, request

from app.utils.MyLogger import GFLogger, MyLoggerFactory
from app.utils.RetDefine import RetDefine
from configs import Config
import xml.etree.ElementTree as ET
import hashlib
from flask.helpers import make_response
from app.utils.XXTea import xxtea_encrypt_text, xxtea_is_matched
from app.utils.RedisClient import RedisClient

logger = MyLoggerFactory().getLogger(__name__)
time_logger = MyLoggerFactory().getLogger('time')
dumps = partial(json.dumps, ensure_ascii=False)

fmtsp = '%Y-%m-%d'
fmtdl = '%Y-%m-%d %H:%M:%S'

def json_res(ret_type=RetDefine.NO_ERR, data=None):
    ret = {"status":ret_type}
    if data:
        ret['data'] = data
    if ret_type != RetDefine.NO_ERR:
        GFLogger.error(ret)
    return dumps(ret)

def send_req(url, data=None):
        if data:
            data = urllib.urlencode(data)
        request = urllib2.Request(url=url, data=data)
        res = urllib2.urlopen(request)
        return res.read()

def send_json(url, data):
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(data, ensure_ascii=False))
    res = urllib2.urlopen(request)
    return res.read()

def md5(data):
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

def gen_ramdon_string(length=10):
    return string.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], length)).replace(' ', '')

def get_now_date():
    return str(int((time.time() * 1000)))

def get_now_time(offset=0, detail=False):
    now = datetime.datetime.now()
    if offset:
        days = datetime.timedelta(days=offset)
        now = now - days
    fmt = fmtdl if detail else fmtsp
    return  now.strftime(fmt)

def timestamp2str(timestamp, detail=False):
    fmt = fmtdl if detail else fmtsp
    return time.strftime(fmt, time.localtime(float(timestamp)))

def str2timestamp(timestr, detail=False):
    fmt = fmtdl if detail else fmtsp
    return time.mktime(time.strptime(timestr, fmt))

def str_offset_timestamp(timestr, offset=0, detail=False):
    dt = datetime.datetime.strptime(timestr, fmtdl if detail else fmtsp)
    if offset:
        days = datetime.timedelta(days=offset)
        dt = dt - days
    return time.mktime(dt.timetuple())

def enum(**enums):
    return type('Enum', (), enums)

def filterMap(data, keys):
    return {key:data[key] for key in keys if key in data}

def xml2dict(text):
    root = ET.fromstring(text)
    for each in root.getiterator("xml"):
        data = each.attrib
        for childNode in each.getchildren():
            data[childNode.tag] = childNode.text
        return data

def is_login(cookie=None, cmd='exists', redis_key=Config.USER_LOGIN_RECORD):
    if not cookie:
        cookie = get_cookie()
    if cmd == "exists":
        return RedisClient().get_slave().exists(redis_key % cookie)
    else:
        return RedisClient().get_slave().get(redis_key % cookie)

def get_cookie(name=Config.COOKIE_NAME):
    return request.cookies.get(name)

def set_login(data, response=None , cookie_name=Config.COOKIE_NAME):
    cookie = gen_ramdon_string(15)
    while not RedisClient().get_master().set(Config.USER_LOGIN_RECORD % cookie, data, ex=Config.ONE_DAY, nx=True):
        pass  # 插入不存在，直到插入成功
    if not response:
        response = make_response()
    response.set_cookie(cookie_name, cookie)
    return response

# 检查登录状态
def is_loged(func):
    @wraps(func)
    def lazy_func(*args, **kwds):
        cookie = get_cookie()
        if cookie and is_login(cookie):
            return func(*args, **kwds)
        else:
            return json_res(RetDefine.NOT_LOGIN)
    return lazy_func

def is_admin_loged(func):
    @wraps(func)
    def lazy_func(*args, **kwds):
        cookie = get_cookie()
        if cookie and is_login(cookie, redis_key=Config.ADMIN_LOGIN_RECORD):
            return func(*args, **kwds)
        else:
            return json_res(RetDefine.NOT_LOGIN)
    return lazy_func
# 动态注入参数
def inject_params(params, can_empty=False):
    def real_decorator(func):
        @wraps(func)
        def lazy_func(*args, **kargs):
            data = {}
            for arg in params:
                if type(arg) == str:
                    data[arg] = request.values.get(arg, None)
                    if not can_empty and not data[arg]:
                        return json_res(101)
                elif type(arg) == tuple:
                    default_val = hasattr(arg[1], '__call__') and arg[1]() or arg[1]
                    data[arg[0]] = request.values.get(arg[0], default_val)
            return func(data, *args, **kargs)
        return lazy_func
    return real_decorator


def check_time(func):
    @wraps(func)
    def lazy_fun(*args, **kargs):
        if Config.CHECK_TIME:
            start = time.clock()
            ret = func(*args, **kargs)
            end = time.clock()
            logger.debug(func.__name__ + " api cost time %f s" % (end - start))
            return ret
        else:
            return func(*args, **kargs)
    return lazy_fun


