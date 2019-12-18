# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:16
"""

# import lib
from datetime import datetime
from decimal import Decimal

from flask import jsonify

from pm_cms.libs.redprint import RedPrint
from pm_cms.libs.response import ResMsg
from flasgger import swag_from

api = RedPrint('project')


@api.route("/")
@swag_from('project.yml')
def index():
    res = ResMsg()
    test_dict = dict(name="张三", age=18)
    res.update(data=test_dict)
    for i in range(10):
        print(i)
    return jsonify(res.data)


@api.route('/type_response')
def test_type_respone():
    res = ResMsg()
    now = datetime.now()
    date = now.date()
    num = Decimal(11.11)
    test_dict = dict(now=now, date=date, num=num)
    res.update(data=test_dict)
    return res.data
