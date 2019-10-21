# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:19
"""

# import lib
import click

from app.model.base import db
from app.model.user import User


def register_init_commands(app):
    @app.cli.command()
    def init():
        pass

    @app.cli.command()
    def fake_super():
        "Create Super User"
        with db.auto_commit():
            user = User()
            user.nickname = 'Super'
            user.password = '123456'
            user.email = '1234@qq.com'
            user.auth = 2
            db.session.add(user)
            click.echo("Create Super User is Done!")
