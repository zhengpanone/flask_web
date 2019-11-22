# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/11/21 10:53
"""

# import lib
from enum import Enum

from pm_cms.model.base import Base, db


class IsOutSourceEnum(Enum):
    YES = 1
    NO = 0


class SeqPlatformEnum(Enum):
    NOVASEQ = 1
    MISEQ = 2
    XTEN = 3


class Pooling(Base):
    pooling_name = db.Column(db.String(80), comment="pooling单")
    outsourcing_business = db.Column(db.Boolean, default=False, comment="是否外包")
    seq_platform = db.Column(db.Integer, comment="测序平台")
    projects = db.relationship('Project', back_populates='pooling')
