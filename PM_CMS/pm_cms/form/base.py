# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/22 10:00
"""

# import lib
from flask_wtf import Form

from pm_cms.libs.error_code import ParameterException


class BaseForm(Form):

    def __init__(self, data):
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        validate = super(BaseForm, self).validate()
        if not validate:
            raise ParameterException(msg=self.errors)
