# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:57
"""

# import lib
from flask import render_template

from app.views import stat


@stat.route("/index")
def index():
    return render_template("stat/index.html")


@stat.route("/food")
def food():
    return render_template("stat/food.html")


@stat.route("/member")
def memebr():
    return render_template("stat/member.html")


@stat.route("/share")
def share():
    return render_template("stat/share.html")
