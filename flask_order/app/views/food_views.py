# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/18 14:56
"""

# import lib
from flask import render_template

from app.views import food


@food.route("/index")
def index():
    return render_template("food/index.html")


@food.route("/info")
def info():
    return render_template("food/info.html")


@food.route("/set")
def set():
    return render_template("food/set.html")


@food.route("/cat")
def cat():
    return render_template("food/cat.html")


@food.route("/cat-set")
def catSet():
    return render_template("food/cat_set.html")
