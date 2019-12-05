# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/21 11:01
"""

# import lib
from pm_cms.libs.error_code import Success
from pm_cms.libs.redprint import RedPrint
from pm_cms.model.pooling import Pooling
from pm_cms.validators.pooling_form import PoolingForm

api = RedPrint('pooling')


@api.route('/', methods=['POST'])
def index():
   
    form = PoolingForm().validate_for_api()

    pooling_name = form.pooling_name.data
    is_outsource = form.is_outsource.data
    seq_platform = form.seq_platform.data
    Pooling.add_pooling(pooling_name, is_outsource, seq_platform)
    return Success(msg="pooling单添加成功")
