# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:16
"""

# import lib
from app.libs.redprint import RedPrint

api = RedPrint('project')


@api.route("/")
def index():
    return "I am API"
