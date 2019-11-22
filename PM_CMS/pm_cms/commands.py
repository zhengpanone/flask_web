# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:19
"""

# import lib
import click

from pm_cms.libs import read_excel
from pm_cms.model.base import db


def register_init_commands(app):
    @app.cli.command()
    def init():
        """init database"""
        click.echo("init db!")
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo("db init success!")

    @app.cli.group()
    def pooling():
        pass

    @pooling.command()
    @click.option('-pooling', required=True, type=click.Path(exists=True, resolve_path=True), help="pooling file path")
    def add(pooling):
        """import pooling to db"""
        click.echo(pooling)
        # print(pooling)
        project_list = read_excel.read_excel(pooling)
        print(project_list)
