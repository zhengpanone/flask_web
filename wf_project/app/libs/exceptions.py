# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/25 9:12
"""

# import lib

from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = "sorry, we make a mistake "
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        super(APIException, self).__init__(msg, None)

        if headers:
            self.headers = headers

    def get_body(self, environ=None):
        body = dict(msg=self.msg,
                    error_code=self.error_code,
                    request=request.method + " " + self.get_url_no_param())
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json")]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split("?")
        return main_path[0]


class ClientTypeException(APIException):
    """
    400 请求参数错误
    401 未授权
    403 禁止访问
    404 未找到资源
    500 服务器产生未知错误
    200 查询成功
    201 创建或更新成功
    204 删除成功
    301 302 重定向
    """
    code = 400
    msg = "client is invalid"
    error_code = 1006
