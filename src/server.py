# /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from app.views.MainView import main_view
from app.views.UserView import user_view
from app.views.PlantView import plant_view
from app.views.TaskView import task_view
from app.utils.mp.MpTimer import MpTimer
import time, threading
from app.utils.Timer import LoopingCall

def configure_blueprints(app):
    app.secret_key = 'qweasd'
    blueprints = {main_view:'/', user_view:'/api/user/', plant_view:'/api/plant/', task_view:'/api/task/' }
    for key in blueprints:
        app.register_blueprint(key, url_prefix=blueprints[key])

def create_app():
    app = Flask(__name__)
    configure_blueprints(app)
    return app

def reload_timer():
    MpTimer().start()

def init_task_timer():
    cur_time = time.time()
    one_day = 86400
    time_flag = one_day - cur_time % one_day
    LoopingCall(time_flag, one_day, reload_timer).start()

init_task_timer()
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
