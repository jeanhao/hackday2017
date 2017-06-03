# coding=UTF-8
from flask import Blueprint

from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params, is_loged
from Configs import POST, GET
from app.service.PlantService import PlantService

plant_view = Blueprint('plant', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)


@plant_view.route("list", methods=GET)
@is_loged
def list_plant():
    return PlantService().list_plant()

@plant_view.route("add", methods=POST)
@is_loged
@inject_params(['pt_type', 'nickname', 'age'])
def add_plant(data):
    return PlantService().add_plant(data)

@plant_view.route("del", methods=POST)
@is_loged
@inject_params(['id'])
def del_plant(data):
    return PlantService().del_plant(data)

@plant_view.route("detail/<_id>", methods=POST)
@is_loged
def detail_plant(_id):
    return PlantService().detail_plant(_id)



