from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect
from flask_moment import Moment

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
moment = Moment()
# Flask-Dropzone还内置了对CSRFProtect扩展的支持，我们可
# 以使用CSRFProtect来添加对上传文件请求的CSRF保护
csrf = CSRFProtect()
dropzone = Dropzone()
avatars = Avatars()
whooshee = Whooshee()


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.anonymous_user = Guest
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = 'Please reauthenticate to access this page'
login_manager.needs_refresh_message_category = 'warning'
