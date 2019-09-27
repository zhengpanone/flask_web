# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:25
"""

# import lib

from flask import Blueprint

pm_bp = Blueprint('views', __name__)
from app.blueprint import views
