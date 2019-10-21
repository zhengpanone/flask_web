# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:42
"""

# import lib
from flask import Blueprint

from app.api.v01 import project, client, token, user


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    project.api.register(bp_v1, url_prefix='/project')
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    user.api.register(bp_v1)
    return bp_v1
