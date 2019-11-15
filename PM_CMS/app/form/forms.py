# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/6 11:31
"""

# import lib
from flask_wtf import FlaskForm
from wtforms import FileField, ValidationError, StringField, SubmitField


class Nonevalidators(object):

    def __init__(self, message):
        self.message = message

    def __call__(self, form, field):
        if field.data == "":
            # StopValidation 不再继续后面的验证  ValidationError 继续后面的验证
            raise ValidationError(self.message)
        return None


class PoolingForm(FlaskForm):
    pooling_name = StringField(label="输入pooling单名称",
                               validators=[Nonevalidators("pooling单不能为空")],
                               render_kw={"class": "form-control m-input m-input--air ",
                                          "placeholder": "Test", "aria-describedby": "basic-addon1"}
                               )

    pooling_file = FileField(validators=[Nonevalidators("上传一个文件")],
                             render_kw={"class": "custom-file-input ", "id": "customFile"})
    submit = SubmitField(label="展示",
                         render_kw={"class": "btn btn-primary", "id": "pooling_excel"})
