# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:57
"""

# import lib
from flask import render_template

from app.views import finance


@finance.route('/index')
def index():
    return render_template('finance/index.html')


@finance.route('/pay-info')
def payInfo():
    return render_template('finance/pay_info.html')


@finance.route('/account')
def account():
    return render_template('finance/account.html')
