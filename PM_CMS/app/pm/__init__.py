# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""

# import lib

from flask import Blueprint

pm = Blueprint('pm', __name__)
from app.pm import views
