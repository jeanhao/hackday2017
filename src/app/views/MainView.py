# coding=UTF-8
from flask import Blueprint

from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params
from Configs import POST


main_view = Blueprint('main', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)

@main_view.route("")
def index():
    return "Hello World!"
