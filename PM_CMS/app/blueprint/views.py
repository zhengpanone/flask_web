# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""

from flask import current_app

from app.blueprint import pm_bp


@pm_bp.route('/')
def test():
    return "Test Flask"


@pm_bp.route("/index")
def index():
    return "Index Page"


@pm_bp.route("/log", methods=["GET"])
def test_log():

    current_app.logger.info("this is info")
    current_app.logger.debug("current_app debug")
    current_app.logger.warning("current_app warning")
    current_app.logger.critical("current_app critical")

    return "test log"
