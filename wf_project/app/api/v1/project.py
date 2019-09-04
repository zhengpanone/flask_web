# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 18:40
"""

# import lib
from app.libs.redprint import RedPrint

api = RedPrint('project')


@api.route('/')
def index():
    return "this is project!"
