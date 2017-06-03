# coding=UTF-8
from flask import Blueprint

from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params
from app.utils.CommonUtils import pack, gen_ramdon_string, gen_ramdon_num
from Configs import POST
from app.service.UserService import UserService
from app.utils import PhoneMessager
from flask.globals import session
from app.utils.RetDefine import RetDefine

user_view = Blueprint('user', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)


@user_view.route("message", methods=POST)
@inject_params(['phone_num', 'nickname'])
def send_message(data):
    verify_code = str(gen_ramdon_num())
    session['verify_code'] = verify_code
    res = PhoneMessager.send_message(data['phone_num'], verify_code)
#     res = PhoneMessager.send_message(data['phone_num'], verify_code, data['nickname'])
    if res:
        return pack()
    else:
        return pack(RetDefine.SEND_ERROR)

@user_view.route("register", methods=POST)
@inject_params(['phone_num', 'password', 'nickname', 'verify_code'])
def register(data):
    if 'verify_code' not in session:
        return pack(RetDefine.VERIFY_CODE_NOT_EXIST)
    elif data['verify_code'] != session['verify_code']:
        return pack(RetDefine.VERIFY_CODE_ERROR)
    data.pop('verify_code')
    return UserService().register(data)

@user_view.route("login", methods=POST)
@inject_params(['phone_num', 'password'])
def login(data):
    return UserService().login(data)

