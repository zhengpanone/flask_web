# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:06
"""

# import lib
import logging.config
import os

from datetime import date

import yaml
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from werkzeug.exceptions import HTTPException

from app.model.base import db
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.settings import config


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask("app")
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_redprints(app)
    register_error(app)
    register_commands(app)
    register_logging(app)
    with app.app_context():
        db.create_all()
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from app.blueprint import pm_bp
    app.register_blueprint(pm_bp)


def register_redprints(app):
    from app.api.v01 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix="/v1")


def register_error(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, APIException):
            return e
        if isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 1007
            return APIException(msg=msg, code=code, error_code=error_code)
        else:
            if not app.config['DEBUG']:
                return ServerError()
            else:
                raise e


def register_logging(app):
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)  # 载入日志配置


def register_commands(app):
    from app.commands import register_init_commands
    register_init_commands(app)
