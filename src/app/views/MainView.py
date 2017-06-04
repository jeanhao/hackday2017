# coding=UTF-8
import hashlib
import json

from flask import Blueprint
from flask.globals import request, session
from flask.helpers import make_response
from werkzeug import redirect
import Configs
from Configs import POST, METHODS
from app.utils.CommonUtils import send_req, xml2dict
from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params
from app.utils.mp.MsgDealer import MsgDealer
from app.service.UserService import UserService


main_view = Blueprint('main_view', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)

local_ip = "114.247.50.2"
gaode_key = "d7b2778364cf4968e18af578be920160"

errorText = '<center><h1>你访问的链接路径不对喔</h1></center>'

@main_view.route('')
def root():
    return errorText

@main_view.route('msg', methods=METHODS)
def msg():
    if request.method == 'GET':
        token = 'bingyan_bbm'
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
        else:
            return errorText
    else:
        rec = request.stream.read()
        data = xml2dict(rec)
        return MsgDealer().deal(data)

# 通过code换取网页授权access_token
@main_view.route('login')
def get_access_token():
    # 到这里表示用户同意授权登陆，拿到了用户的code
    code = request.values.get('code')
    state = request.values.get('state')
    # 网页access token 是一次性的，每次都要重复获取
    access_token_url = Configs.WEB_ACCESS_TOKEN_URL % code
    res = send_req(access_token_url)
    token_data = json.loads(res)
    if 'errcode' in token_data:
        print token_data['errmsg']
        return 'fail token'
    access_token = token_data['access_token']
    openid = token_data['openid']
    # 拉取用户信息
    user_info_url = Configs.USER_BASE_INFO_URL % (access_token, openid)
    res = send_req(user_info_url)
    user_data = json.loads(res)
    if 'errcode' in user_data:
        print token_data['errmsg']
        return 'fail user'
    # 已经拉取到用户信息，跳转到原来界面
#     response = set_login(json.dumps({"nickname": user_data['nickname'], 'openid':openid}))
    session['user'] = user_data
    url = "%s%s" % (request.url_root, state)
    return redirect(url)

@main_view.route('test_login')
def test_login():
    res = make_response('ok')
    user = {"openid": 'o-UJCxAoz4qdPzxJL2N-us54JXc0', 'nickname':u'小三', 'images':'test'}
    session['user'] = user
    return res


@main_view.route('public/<site>')  # 这里进入访问特定界面
@main_view.route('public/<site>/<_id>')
def route(site, _id=None):
    if site not in ['index', 'list']:  # ['pub', 'help', 'market', 'pubsell', 'buy']
        return "访问地址出错，请检查"
    # 检查用户状态
    if 'user' in session:
        session['user']

    else:
        url = Configs.AUTH_BASE_URL + site
        if id:
            url = "%s/%s" % (url, id)
        return redirect(url)

@main_view.route("user_info")
def user_info():
    return json.dumps(session['user'])

@main_view.route("get_ip")
def get_ip():
    return request.remote_addr


@main_view.route("pos", methods=METHODS)
def pos():
#     ip = request.values.get('ip')
    ip = local_ip
    if not ip:
        return 'ip required'
    else:
        get_pos(ip)

def get_pos(ip):
    url = "http://restapi.amap.com/v3/ip?key=%s&ip=%s" % (gaode_key, ip)
    return json.loads(send_req(url))

@main_view.route("weather", methods=METHODS)
def weather():
#     ip = request.values.get('ip')
    ip = local_ip
    if not ip:
        return 'ip required'
    else:
        pos = get_pos(ip)
        url = "http://restapi.amap.com/v3/weather/weatherInfo?key=%s&city=%s" % (gaode_key, pos['adcode'])
        return send_req(url)

