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


class DeleteSuccess(Success):
    code = 202
    msg = 'Delete Success!'
    error_code = -1


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


class NotFound(APIException):
    code = 404
    msg = ''
    error_code = 1001


class AuthFailed(APIException):
    code = 401  # 授权失败
    error_code = 1005
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403  # 禁止访问
    error_code = 1004
    msg = 'forbidden, not in scope'
