# -*- coding: utf-8 -*-
from datetime import datetime

from flasky.extensions import db
from flasky.models.base import Base


class Post(Base):
    __tablename__ = 'post'
    body = db.Column(db.Text, comment="内容")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow(), comment='时间')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
