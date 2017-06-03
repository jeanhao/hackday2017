# coding=UTF-8
from flask import Blueprint

from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params
from Configs import POST, METHODS
from flask.globals import request
from app.utils.CommonUtils import send_req
import json


main_view = Blueprint('main', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)

local_ip = "114.247.50.2"
gaode_key = "d7b2778364cf4968e18af578be920160"

@main_view.route("")
def index():
    return "Hello World!"

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

