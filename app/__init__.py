# -*- coding: UTF-8 -*-
"""
Created on 2016/6/2

@author: mavericks
"""

from flask import Flask
from config import config
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap

mongo = PyMongo()
bootstrap = Bootstrap()


def create_app(config_name='defalut'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mongo.init_app(app)
    bootstrap.init_app(app)

    from server import server as server_blueprint
    from self import self as self_buleprint

    app.register_blueprint(server_blueprint)
    app.register_blueprint(self_buleprint, url_prefix='/self')

    return app


