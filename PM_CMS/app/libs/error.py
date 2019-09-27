# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 17:02
"""

# import lib
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry , we make a mistake !'
    error_code = 999  # 未知错误

    def __init__(self, msg=None, code=None, err0r_code=None):
        if code:
            self.code = code
        if err0r_code:
            self.error_code = code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(msg=self.msg,
                    error_code=self.error_code,
                    request=request.method + ' ' + self.get_url_no_param()
                    )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
