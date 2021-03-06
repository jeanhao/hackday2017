# coding=UTF-8
from functools import wraps
import os

from flask.globals import session, request

from app.utils.CommonUtils import pack
from app.utils.RetDefine import RetDefine


if os.name == 'nt':
    DEFAULT_TEMPLATE_FOLDER = 'E:/eclipse-multi/HackDay/public'
else:
    DEFAULT_TEMPLATE_FOLDER = '/home/hustonline/zenghao/hackday_plant/public'

# 检查登录状态
def is_loged(func):
    @wraps(func)
    def lazy_func(*args, **kwds):
#         user = {"open_id": 'o-UJCxAoz4qdPzxJL2N-us54JXc0', 'nickname':u'小三', 'images':'test'}
#         session['user'] = user
        if 'user' in session:
            return func(*args, **kwds)
        else:
            return pack(RetDefine.USER_NOT_LOGIN)
    return lazy_func

# 动态注入参数，并检查是否合法
def inject_params(params, can_empty=False):
    def real_decorator(func):
        @wraps(func)
        def lazy_func(*args, **kargs):
            req_data = request.get_json() or {}
            data = {}
            for arg in params:
                if type(arg) == str:
                    data[arg] = req_data.get(arg, None)
                    if not can_empty and data[arg] == None:
                        return pack(RetDefine.LACK_ARGS)
                elif type(arg) == tuple:
                    default_val = hasattr(arg[1], '__call__') and arg[1]() or arg[1]
                    data[arg[0]] = req_data.get(arg[0], default_val)
            return func(data, *args, **kargs)
        return lazy_func
    return real_decorator

