# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""
from app.blueprint import pm_bp


@pm_bp.route('/')
def test():
    return "Test Flask"


@pm_bp.route("/index")
def index():
    return "Index Page"
