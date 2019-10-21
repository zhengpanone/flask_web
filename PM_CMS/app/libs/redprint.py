# -*- coding:utf-8 -*-

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 14:41
"""


class RedPrint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            # 取字典的value 当key为endpoint,如不存在则取f.__name__ 视图函数的名字
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
