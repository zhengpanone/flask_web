# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:23
"""

# import lib
from flask import render_template

from app.views import account


@account.route('/index')
def index():
    return render_template('account/index.html')


@account.route('/info')
def info():
    return render_template('account/info.html')


@account.route('/set')
def set():
    return render_template('account/set.html')
