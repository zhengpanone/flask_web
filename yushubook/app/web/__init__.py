# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

'''蓝图管理'''
# 蓝图blueprint
web = Blueprint('web', __name__)
print('id为' + str(id(web)) + '的蓝图注册路由')


# AOP 面向切面编程
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# @web.app_errorhandler(500)
# def not_found(e):
#     return render_template('404.html'), 500


from app.web import book, auth, drift, gift, main, wish
