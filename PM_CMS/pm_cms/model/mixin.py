# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/12/5 15:10
"""


# import lib

class ReprMixin:

    def __repr__(self):
        s = self.__class__.__name__ + '('

        for k, v in self.__dict__.items():
            if not k.startwith('_'):
                s += '{}={}, '.format(k, v)

        s = s.rstrip(',') + ')'
        return s
