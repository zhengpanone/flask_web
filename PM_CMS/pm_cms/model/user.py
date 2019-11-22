# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/27 15:37
"""

# import lib

from werkzeug.security import generate_password_hash, check_password_hash

from pm_cms.libs.error_code import NotFound, AuthFailed
from pm_cms.model.base import Base, db


class User(Base):
    email = db.Column(db.String(24), unique=True, nullable=False, comment="邮箱")
    nickname = db.Column(db.String(24), unique=True, comment="昵称")
    auth = db.Column(db.SmallInteger, default=1, comment="用户角色")
    _password = db.Column('password', db.String(120), comment="密码")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        """
        校验邮箱密码是否正确
        :param email:       邮箱
        :param password:    密码
        :return: {'uid':'id','scope':'scope'}
        """
        user = User.query.filter_by(email=email).first_or_404(description="user not found")
        if not user:
            raise NotFound(msg="user not found")
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        """
        校验密码是否正确
        :param raw:
        :return:
        """
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
