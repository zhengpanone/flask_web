# -*- coding: utf-8 -*-
import os

from flask import Flask

from flasky.blueprints import config_blueprint
from flasky.extensions import login_manager, bootstrap, moment, db, migrate, mail
from flasky.models.user import User, Role, Permission
from flasky.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('flasky')
    app.config.from_object(config[config_name])

    register_extentsions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_commands(app)

    with app.app_context():
        db.create_all()
    return app


def register_extentsions(app):
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    # flask-migrate添加flask db命令和几个子命令，在新项目中可以使用init子命令添加数据库迁移命令支持 flask db init
    migrate.init_app(app, db=db)


def register_blueprints(app):
    config_blueprint(app)


def register_error_handlers(app):
    pass


def register_shell_context(app):
    """
    每次启动shell 会话都要导入数据库实例和模型，flask shell 命令自动导入这些对象，
    app.shell_context_processor装饰器创建并注册以一个shell上下文处理器
    :param app:
    :return:
    """

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role)


def register_commands(app):
    from flasky.commands import register_init_commands
    register_init_commands(app)
