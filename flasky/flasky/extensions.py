# -*- coding: utf-8 -*-
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# 扩展库实例化

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'user.login'  # 设置登录页面的端点
login_manager.login_message = '欢迎登录'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'
