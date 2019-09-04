# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
toolbar = DebugToolbarExtension()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    """用户加载函数"""
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.session_protection = 'strong'  # 可以设为None、basic、strong
login_manager.login_view = 'auth.login'  # 设置登录页面的端点
login_manager.login_message_category = 'warning'


