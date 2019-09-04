# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from flask import Flask, render_template, session
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from bluelog.blueprints import blog_bp, admin_bp, auth_bp
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager, csrf, toolbar, migrate
from bluelog.models import Admin, Category, Comment
from bluelog.settings import config


def create_app(config_name=None):
    """工厂函数接收配置名称作为参数，指创建其他对象的对象，通常是一个返回其他类的对象的函数或方法
    当工厂函数被调用后，先创建一个特定配置类的程序实例，然后·执行一系列注册函数为程序实例注册扩展、
    蓝图、错误处理、上下文处理器、请求处理器...
    """
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)

    return app


def register_logging(app):
    pass


def register_extensions(app):
    """初始化扩展程序"""
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # app.permanent_session_lifetime = timedelta(minutes=1)  # 设置session 过期时间
    csrf.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app)


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    """注册shell上下文处理函数"""

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    """处理模板上下文"""

    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """自定义CSRF错误响应"""
        return render_template('error/400.html', description=e.description), 400


def register_commands(app):
    """注册自定义shell命令"""
    from bluelog.commands import register_init_commands
    register_init_commands(app)
