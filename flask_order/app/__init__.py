# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 11:24
"""

# import lib
import os

from flask import Flask

from app.common.libs.url_mainager import UrlManager
from app.extensions import db
from app.settings import config


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name, template_folder=template_folder, root_path=root_path,
                                          static_folder=None)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Application(__name__, template_folder=os.getcwd() + "/app/templates", root_path=os.getcwd() + "/app")
    app.config.from_object(config[config_name])
    # register_extensions(app)
    register_blueprints(app)
    register_template_methods(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from app.views import user
    from app.views import route_static
    from app.views import index
    from app.views import account
    from app.views import finance
    from app.views import food
    from app.views import stat
    from app.views import member
    app.register_blueprint(user)
    app.register_blueprint(route_static)
    app.register_blueprint(index)
    app.register_blueprint(account)
    app.register_blueprint(finance)
    app.register_blueprint(food)
    app.register_blueprint(stat)
    app.register_blueprint(member)


def register_template_methods(app):
    app.add_template_global(UrlManager.build_static_url, 'buildStaticUrl')
    app.add_template_global(UrlManager.build_url, 'buildUrl')
