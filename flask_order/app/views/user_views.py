# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 11:30
"""

# import lib
from flask import render_template

from app.views import user


@user.route('/login')
def login():
    return render_template('user/login.html')


@user.route('/edit')
def edit():
    return render_template('user/edit.html')


@user.route('/reset-pwd')
def reset_pwd():
    return render_template('user/reset_pwd.html')
