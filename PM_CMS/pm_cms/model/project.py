# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 10:00
"""

# import lib
from sqlalchemy import ForeignKey

from pm_cms.model.base import Base, db

tags = db.Table('project_tag',
                db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                )


class Project(Base):
    contract_name = db.Column(db.String(80), comment="合同名称")
    contract_num = db.Column(db.String(80), comment="合同编号")

    pooling_id = db.Column(db.Integer, ForeignKey('pooling.id'), comment='pooling单ID')

    project_name = db.Column(db.String(80), comment="任务单名称")
    project_num = db.Column(db.String(80), comment="项目编号")

    sample_name = db.Column(db.String(80), comment="样本名称")
    library_name = db.Column(db.String(80), comment="文库号")
    nucleic_name = db.Column(db.String(80), comment="核酸编号")
    library_type = db.Column(db.String(80), comment="文库类型")

    index_i5 = db.Column(db.String(80), comment="I5 index")
    index_i5_name = db.Column(db.String(80), comment="I5 index name")
    index_i7 = db.Column(db.String(80), comment="I7 index")
    index_i7_name = db.Column(db.String(80), comment="I7 index name")
    library_is_true = db.Column(db.Boolean, default=False, comment="文库是否合格")

    seq_type = db.Column(db.String(80), comment="测序策略")
    p_type = db.Column(db.Integer, comment="项目类型")

    lane = db.Column(db.String(80), comment="上机lane")
    output = db.Column(db.String(80), comment="数据产出")

    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('projects', lazy='dynamic'))


class Tag(Base):
    name = db.Column(db.String(80), comment="标签名")
