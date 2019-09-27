# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:15
"""

# import lib
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQLALCHEMY_TRACK_MODIFICATIONS = False


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "adsfdf")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/pm_dev"
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
