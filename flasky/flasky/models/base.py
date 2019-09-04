# -*- coding: utf-8 -*-
from datetime import datetime

from flasky.extensions import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True, comment="编号")
    create_time = db.Column('create_time', db.DateTime, index=True, default=datetime.now(), comment="创建时间")
    status = db.Column('status', db.Boolean, default=True, comment='状态，0为删除，1为未删除')
