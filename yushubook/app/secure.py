# -*- coding: utf-8 -*-

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@10.10.20.41:3306/fisher'
# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@10.10.100.2:7821/fisher'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

SECRET_KEY = 'qaxzdsdasfasdfafdaf'

# Email 配置

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USER_TSL = False
MAIL_USERNAME = '1216031280@qq.com'
MAIL_PASSWORD = 'fcjfvgviczczbacd'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书<hello@yushu.im>'
