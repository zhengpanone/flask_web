# -*- coding: utf-8 -*-
import os

import click
from flask import Flask

from albumy.blueprints import auth_bp, main_bp, user_bp, ajax_bp, admin_bp
from albumy.extensions import db, mail, login_manager, csrf, bootstrap, moment, dropzone, avatars, whooshee
from albumy.models import Role
from albumy.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')

    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)
    whooshee.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')
    app.register_blueprint(admin_bp, url_perfix='/admin')


def register_commands(app):
    @app.cli.command()
    def init():
        """Initialize Albumy."""

        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Done')
        # whooshee.reindex() flask-whooshee 重建索引
