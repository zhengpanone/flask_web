# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 15:25
"""

# import lib
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from pm_cms.libs.enums import ClientTypeEnum
from pm_cms.model.user import User
from pm_cms.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message="账号不能为空"),
                                      length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired("客户端类型不能为空")])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client  # 将type.data赋值为枚举类型


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message="邮箱不符合规则")])
    secret = StringField(validators=[DataRequired('密码不正确'), Regexp(r'[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired('昵称不能为空'), length(min=2, max=22)])

    def validate_account(self, value):
        """
        验证邮箱是否注册
        :param value:
        :return:
        """
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()
