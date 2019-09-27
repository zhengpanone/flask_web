# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 15:37
"""

# import lib
from werkzeug.security import generate_password_hash

from app.model.base import Base, db


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(24), unique=True, nullable=False, comment="邮箱")
    nickname = db.Column(db.String(24), unique=True, comment="昵称")
    _password = db.Column('password', db.String(120), comment="密码")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret, ):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)
