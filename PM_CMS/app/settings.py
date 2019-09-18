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


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "adsfdf")


class DevelopmentConfig(BaseConfig):
    MONGO_HOST = "localhost"
    MONGO_PORT = "27017"
    MONGO_DBNAME = "pmdb_dev"
    MONGO_URI = "mongodb://localhost:27017/pmdb_dev"


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
