# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/21 11:01
"""

# import lib
from flask import request

from pm_cms.form.pooling import PoolingForm
from pm_cms.libs.redprint import RedPrint
from pm_cms.model.response import ResMsg

api = RedPrint('pooling')


@api.route('/', methods=['POST'])
def index():
    data = request.json
    form = PoolingForm(data=data)
    res = ResMsg()
    form.validate_for_api()
    return res.data
