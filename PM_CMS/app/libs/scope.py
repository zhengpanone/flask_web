# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/29 14:46
"""


# import lib
class Scope:
    allow_api = set()
    allow_module = set()
    forbidden = set()

    def __add__(self, other):  # 运算符重载
        self.allow_api = self.allow_api + other.allow_api
        self.allow_module = self.allow_module + other.allow_module
        self.forbidden = self.forbidden + other.forbidden
        return self


class AdminScope(Scope):
    allow_api = set('v1.super_get_user')

    def __init__(self):
        self + UserScope()


class UserScope(Scope):
    allow_api = set()
    allow_module = set()


class SuperScope:
    allow_api = []

    def __init__(self):
        self.add()

    def add(self, other):
        pass


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
