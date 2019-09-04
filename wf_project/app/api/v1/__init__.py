# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 18:39
"""

# import lib
from flask import Blueprint
from app.api.v1 import user, project, client


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    project.api.register(bp_v1)
    client.api.register(bp_v1)
    return bp_v1
