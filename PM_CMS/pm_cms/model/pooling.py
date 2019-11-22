# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/21 10:53
"""

# import lib

from pm_cms.model.base import Base, db


class Pooling(Base):
    pooling_name = db.Column(db.String(80), comment="pooling单")
    is_outsource = db.Column(db.Boolean, default=False, comment="是否外包")
    seq_platform = db.Column(db.Integer, comment="测序平台")
    projects = db.relationship('Project', backref='pooling')

    @staticmethod
    def add_pooling(pooling_name, is_outsource, seq_platform):
        with db.auto_commit():
            pooling = Pooling()
            pooling.pooling_name = pooling_name
            pooling.is_outsource = is_outsource
            pooling.seq_platform = seq_platform
            db.session.add(pooling)
