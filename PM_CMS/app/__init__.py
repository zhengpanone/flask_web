# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:06
"""

# import lib
import os

from flask import Flask

from app.extensions import db
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask("app")
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    with app.app_context():
        db.create_all()
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from app.blueprint import pm_bp
    app.register_blueprint(pm_bp, url_prefix='/pm')


def register_logging(app):
    pass
