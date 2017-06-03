# coding=UTF-8
from flask import Blueprint

from app.views.BaseView import DEFAULT_TEMPLATE_FOLDER, inject_params, is_loged
from Configs import POST, GET
from app.service.PlantService import PlantService
from app.service.TaskService import TaskService
from flask.globals import request

task_view = Blueprint('task', __name__, url_prefix="/" , template_folder=DEFAULT_TEMPLATE_FOLDER)

@task_view.route("tag/list", methods=GET)
@is_loged
def list_tag():
    return TaskService().list_tag()

@task_view.route("problem/list", methods=GET)
@is_loged
@inject_params(['tags'])
def list_problem(data):
    tags = data.get('tags')
    return TaskService().list_problem(tags)

@task_view.route("problem/answer", methods=POST)
@is_loged
def answer_problem():
    problems = request.get_json()
    return TaskService().answer_problem(problems)


