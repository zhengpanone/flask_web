# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 15:22
"""

# import lib
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101
    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201


class IsOutSourceEnum(Enum):
    YES = 1
    NO = 0


class SeqPlatformEnum(Enum):
    NOVASEQ = 1
    MISEQ = 2
    XTEN = 3


class TypeEnum(Enum):
    HEALTH = 0  # 健康
    SCIENTIFIC = 1  # 科研
