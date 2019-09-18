# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 10:00
"""


# import lib


class Seq_Platform:
    NOVSEQ = 1
    MISEQ = 2
    XTEN = 3


class Project():
    def __init__(self, project_name, sample_name, nucleic_id, library_type, pooling_num, index_i5, index_i7,
                 library_num, library_is_true, project_num, seq_platform, lane_num, data_output):
        self.project_name = project_name  # 任务单名称
        self.sample_name = sample_name  # 样本名称
        self.nucleic_id = nucleic_id  # 核酸编号
        self.library_type = library_type  # 文库类型
        self.pooing_num = pooling_num  # pooling数量
        self.index_i5 = index_i5  # I5 index
        self.index_i7 = index_i7  # I7 index
        self.library_num = library_num  # 文库号
        self.library_is_true = library_is_true  # 文库是否合格
        self.project_num = project_num  # 项目编号
        self.seq_platform = seq_platform  # 测序平台
        self.lane_num = lane_num  # lane信息
        self.data_output = data_output  # 数据产出

    def add_pooling(self):
        pass
