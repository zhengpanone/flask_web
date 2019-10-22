# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/10/22 21:27
"""


# import lib

class ResponseCode:
    SUCCESS = 0  # 成功
    FAIL = -1  # 失败
    NO_RESOURCE_FOUND = 40001  # 未找到资源
    INVALID_PARAMETER = 40002  # 参数无效
    ACCOUNT_OR_PASS_WORD_ERR = 40003  # 账户或密码


class ResponseMessage:
    SUCCESS = "成功"
    FAIL = "失败"
    NO_RESOURCE_FOUND = "未找到资源"
    INVALID_PARAMETER = "参数无效"
    ACCOUNT_OR_PASS_WORD_ERR = "账户或密码错误"
