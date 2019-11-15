# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/10/31 15:11
"""

# import lib
import xlrd

from app.model.project import Project


def read_excel(excel_path):
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_index(1)
    print(table)
    row_list = []
    name_list = []
    for i in range(table.nrows):
        if i == 0:
            name_list = list(range(len(table.row_values(i, start_colx=0, end_colx=None))))
            for x, y in enumerate(table.row_values(i, start_colx=0, end_colx=None)):
                name = y.strip()
                if "项目编号" == name:
                    name_list[x] = "project_num"
                elif "结题报告样本名称" == name:
                    name_list[x] = "sample_name"
                elif "任务单名称" == name:
                    name_list[x] = "project_name"
                elif "样本编号" == name:
                    name_list[x] = "nucleic_name"
                elif "文库类型" == name:
                    name_list[x] = "library_type"
                elif "测序策略" == name:
                    name_list[x] = "seq_type"
                elif "pooling数据量" == name:
                    name_list[x] = ""
                elif "I5_Index" == name:
                    name_list[x] = "index_i5"
                elif "I5_Index序列" == name:
                    name_list[x] = "index_i5_name"
                elif "文库号" == name:
                    name_list[x] = "library_name"
                elif "文库是否合格" == name:
                    name_list[x] = "library_is_true"
                elif "任务单数据量" == name:
                    name_list[x] = ""
        else:
            project_list = table.row_values(i, start_colx=0, end_colx=None)
            project_dict = dict(zip(name_list, project_list))
            del_keys = []
            for k, v in project_dict.items():
                if k == "library_is_true":
                    project_dict[k] = True if v == "合格" else False
                if not hasattr(Project, str(k)):
                    del_keys.append(k)

            for del_key in del_keys:
                project_dict.pop(del_key)
            row_list.append(project_dict)
    return row_list
