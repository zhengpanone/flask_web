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
from werkzeug.exceptions import HTTPException

from app.extensions import db
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask("app")
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_redprints(app)
    register_error(app)
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
    pass
