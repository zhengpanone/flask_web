# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 10:00
"""

# import lib
from enum import Enum

from app.extensions import db
from app.model.base import Base


class SeqPlatform(Enum):
    NOVSEQ = 1
    MISEQ = 2
    XTEN = 3


class Project(Base):
    project_name = db.Column(db.String(80), comment="任务单名称")
    sample_name = db.Column(db.String(80), comment="样本名称")
    library_name = db.Column(db.String(80), comment="文库号")
    nucleic_name = db.Column(db.String(80), comment="核酸编号")
    library_type = db.Column(db.String(80), comment="文库类型")
    pooing_name = db.Column(db.String(80), comment="pooling单")
    index_i5 = db.Column(db.String(80), comment="I5 index")
    index_i7 = db.Column(db.String(80), comment="I7 index")
    library_is_true = db.Column(db.Boolean, default=True, comment="文库是否合格")
    project_num = db.Column(db.String(80), comment="项目编号")
    seq_platform = db.Column(db.String(80), comment="测序平台")
    lane = db.Column(db.String(80), comment="测序平台")
    output = db.Column(db.String(80), comment="数据产出")
    outsourcing_business = db.Column(db.Boolean, default=False, comment="是否外包")

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), comment="项目类型ID")
    category = db.relationship('Category', back_populates='project')

    def add_pooling(self):
        pass


class Category(Base):
    name = db.Column(db.String(80), comment="项目类型")
    projects = db.relationship("Project", back_populates='category')
