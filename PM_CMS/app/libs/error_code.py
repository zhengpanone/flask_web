# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 16:53
"""

# import lib

from app.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'OK!'
    error_code = 0


class ServerError(APIException):
    code = 500
    msg = 'sorry we made a mistake !'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'parameter is error'
    error_code = 1000
