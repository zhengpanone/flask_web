# -*- coding: utf-8 -*-
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    ALBUMY_ADMIN_EMAIL = os.getenv('ALBUMY_ADMIN', '1216031280@qq.com')
    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')

    ALBUMY_PHOTO_SIZE = {'small': 400, 'medium': 800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']: '_s',  # thumbnail
        ALBUMY_PHOTO_SIZE['medium']: '_m',  # display
    }

    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)  # 小、中、大三个尺寸

    SECRET_KEY = os.getenv('SECRET_KEY', 'adfadsfdcfad')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 允许上传的文件大小
    DROPZONE_ALLOWED_FILE_CUSTOM = True  # 自定义允许的文件类型，首先需要将配置键 DROPZONE_ALLOWED_FILE_CUSTOM设为True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*, .pdf, .txt'  # 允许上传的文件类型 由文件MIME类型和后缀名组成的字符串（使用分号隔开）
    DROPZONE_ENABLE_CSRF = True
    # DROPZONE_SERVE_LOCAL = True  # 配置使用本地资源css、js


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
