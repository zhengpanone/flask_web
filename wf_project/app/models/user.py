# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 22:05
"""

# import lib
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash


class User():
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    _password = Column(String(1000), 'password')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        pass
