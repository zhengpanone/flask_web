# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:16
"""

# import lib
from flask import jsonify

from app.libs.redprint import RedPrint
from app.model.response import ResMsg

api = RedPrint('project')


@api.route("/")
def index():
    res = ResMsg()
    test_dict = dict(name="张三", age=18)
    res.update(data=test_dict)
    return jsonify(res.data)
