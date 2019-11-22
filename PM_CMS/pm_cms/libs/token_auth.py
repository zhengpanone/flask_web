# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/29 9:43
"""

# import lib
from flask import g
from flask_httpauth import HTTPBasicAuth

from pm_cms.api.v01.token import verify_auth_token

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True
