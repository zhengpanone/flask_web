# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 21:52
"""

# import lib
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length

from app.libs.enums import ClientTypeEnum


class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(6, 30)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def vaildate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
