# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/5/6 18:07
"""

# import lib
from random import randint

from faker import Faker

from flasky.extensions import db
from flasky.models.post import Post
from flasky.models.user import User


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IndentationError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()

    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 user=u)
        db.session.add(p)
        db.session.commit()
