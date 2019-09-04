# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 21:36
"""

# import lib
from flask import request

from app.libs.redprint import RedPrint
from app.validators.forms import ClientForm

api = RedPrint('client')


@api.route('/register', methods=['POST'])
def create_client():
    data = request.json
    form = ClientForm(data=data)
    if form.validate():
        pass
    pass
