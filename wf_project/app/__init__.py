# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 18:35
"""

# import lib
import os

from flask import Flask

from app.extensions import db
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
        print(config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix="/v1")


def register_extensions(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
