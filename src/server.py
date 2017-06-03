# /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from app.views.MainView import main_view
from app.views.UserView import user_view
from app.views.PlantView import plant_view

def configure_blueprints(app):
    app.secret_key = 'qweasd'
    blueprints = {main_view:'/', user_view:'/api/user/', plant_view:'/api/plant/'}
    for key in blueprints:
        app.register_blueprint(key, url_prefix=blueprints[key])

def create_app():
    app = Flask(__name__)
    configure_blueprints(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
