# -*- coding: utf-8 -*-
from flask import Blueprint

blog_bp = Blueprint('blog', __name__, template_folder='templates')
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

from bluelog.blueprints import admin, blog, auth
