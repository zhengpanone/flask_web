# -*- coding: utf-8 -*-
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint("main", __name__)
user_bp = Blueprint('user', __name__)
ajax_bp = Blueprint('ajax', __name__)
admin_bp = Blueprint('admin', __name__)

from albumy.blueprints import auth
from albumy.blueprints import main
from albumy.blueprints import user
from albumy.blueprints import ajax
from albumy.blueprints import admin_bp
