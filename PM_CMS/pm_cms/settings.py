# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:15
"""

# import lib
import os
import pathlib

import mysql.connector

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "adsfdf")
    JSON_AS_ASCII = False
    cwd_dir = pathlib.Path(__file__).resolve().parent

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True
    LOGGING_CONFIG_PATH = cwd_dir.resolve() / 'config/logging.yaml'
    LOGGING_PATH = os.path.join(basedir, './logs')
    MSG_PATH = cwd_dir.resolve() / 'config/msg.yaml'
    UPLOAD_PATH = os.path.join(basedir, 'uploads')


class DevelopmentConfig(BaseConfig):
    TOKEN_EXPIRATION = 30 * 24 * 3600
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@127.0.0.1:3306/pm_dev"
    # SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
