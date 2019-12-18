# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:16
"""

# import lib
from flask import send_from_directory, current_app

from app.views import route_static


@route_static.route('/<path:filename>')
def index(filename):
    return send_from_directory(current_app.root_path + '/static/', filename)
