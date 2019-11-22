# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/21 11:06
"""

# import lib
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from pm_cms.form.base import BaseForm
from pm_cms.model.pooling import IsOutSourceEnum, SeqPlatformEnum


class PoolingForm(BaseForm):
    pooling_name = StringField(validators=[DataRequired(message="pooling单不能为空")])
    is_outsource = IntegerField(validators=[DataRequired(message="外包为1, 不外包为0")])
    seq_platform = IntegerField(validators=[DataRequired(message="测序平台 Novaseq为1,Miseq为2,Xten为3")])

    def validate_is_outsourcing(self, value):
        try:
            is_outsource = IsOutSourceEnum(value.data)
        except ValueError as e:
            raise e
        self.is_outsource.data = is_outsource

    def validate_seq_platform(self, value):
        try:
            seq_platform = SeqPlatformEnum(value.data)
        except ValueError as e:
            raise e
        self.seq_platform = seq_platform
