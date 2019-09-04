# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/5/5 17:29
"""

# import lib
from datetime import timedelta


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = "qazwsx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # Mail
    MAIL_SERVER = 'smtp.qq.com'  # mail的主机或IP地址
    MAIL_POST = 465  # mail端口
    MAIL_USE_TLS = False  # 启用传输层安全
    MAIL_USE_SSL = False  # 启用安全套接层
    MAIL_USERNAME = '1216031280@qq.com'  # 邮箱账户
    MAIL_PASSWORD = 'fcjfvgviczczbacd'  # 邮箱密码
    FLASK_MAIL_SUBJECT_PREFIX = ''
    FLASKY_MAIL_SENDER = '1216031280@qq.com'

    # Cookie
    REMEMBER_COOKIE_DURATION = timedelta(days=1)


# 测试配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flasky_testing?charset=utf8'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flasky?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/development?charset=utf8'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
