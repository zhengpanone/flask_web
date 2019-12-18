# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 11:25
"""

# import lib
from flask import Blueprint

route_static = Blueprint('static', __name__)
user = Blueprint('user', __name__, url_prefix='/user')
index = Blueprint('index', __name__)
account = Blueprint('account', __name__, url_prefix='/account')
finance = Blueprint('finance', __name__, url_prefix='/finance')
food = Blueprint('food', __name__, url_prefix='/food')
member = Blueprint('member', __name__, url_prefix='/member')
stat = Blueprint('stat', __name__, url_prefix='/stat')
from app.views import user_views
from app.views import stiatc
from app.views import index_views
from app.views import account_views
from app.views import finance_views
from app.views import food_views
from app.views import member_views
from app.views import stat_views
