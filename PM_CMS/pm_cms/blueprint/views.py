# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""

from pm_cms.blueprint import pm_bp


@pm_bp.route('/')
def index():
    return ''


@pm_bp.route('/import_project.html', methods=["POST", 'GET'])
def import_project():
    return ''


@pm_bp.route("/upload_file", methods=["POST", 'GET'])
def upload_file():
    return ''
