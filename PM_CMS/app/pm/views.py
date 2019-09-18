# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""
from app.pm import pm


@pm.route('/test')
def test():
    return "Test Flask"
