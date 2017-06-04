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
def list_problem():
    return TaskService().list_problem(request.values.get('tags'))

@task_view.route("problem/answer", methods=GET)
@is_loged
def answer_problem():
    problems = request.values.get('problems').split(",")
    return TaskService().answer_problem(problems)

@task_view.route("answer/confirm", methods=POST)
@is_loged
@inject_params(['has_weekend', 'week_size', 'answers'])
def comfirm_answer(data):
    return TaskService().comfirm_answer(data)

@task_view.route("answer/list", methods=GET)
@is_loged
def list_answer():
    return TaskService().list_answer()

