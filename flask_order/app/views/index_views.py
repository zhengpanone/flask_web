# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:23
"""

# import lib
from flask import render_template

from app.views import index


@index.route('/')
def index():
    return render_template('index/index.html')
