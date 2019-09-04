# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from flask_mail import Mail

'''app初始化'''
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__, static_folder='static')  # 设置静态文件位置
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    mail.init_app(app)
    # db.create_all(app=app)方法一
    with app.app_context():  # 方法二
        db.create_all()

    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
