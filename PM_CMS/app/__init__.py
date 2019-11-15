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

import yaml
from flask import Flask
from werkzeug.exceptions import HTTPException

from app.extensions import migrate, dropzone
from app.libs.core import JSONEncoder
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.model import user, project
from app.model.base import db
from app.settings import config


def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf = yaml.safe_load(f.read())
    return cf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    # app = Flask("app")
    app = Flask(__name__)
    # 返回json格式转换
    app.json_encoder = JSONEncoder
    app.config.from_object(config[config_name])
    cf = read_yaml(app.config['MSG_PATH'])
    app.config.update(cf)
    register_extensions(app)
    register_blueprints(app)
    register_redprints(app)
    register_error(app)
    register_shell_context(app)
    register_commands(app)
    register_logging(app)
    with app.app_context():
        db.create_all()
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    dropzone.init_app(app)


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


def register_shell_context(app):
    """注册shell上下文处理函数
    """

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, model=[user, project])


def register_logging(app):
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)  # 载入日志配置


def register_commands(app):
    from app.commands import register_init_commands
    register_init_commands(app)
