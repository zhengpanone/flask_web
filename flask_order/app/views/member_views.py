# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:56
"""

# import lib
from flask import render_template

from app.views import member


@member.route("/index")
def index():
    return render_template("member/index.html")


@member.route("/info")
def info():
    return render_template("member/info.html")


@member.route("/set")
def set():
    return render_template("member/set.html")


@member.route("/comment")
def comment():
    return render_template("member/comment.html")
