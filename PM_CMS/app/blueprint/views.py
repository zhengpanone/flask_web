# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""
import os

from flask import current_app, request, redirect, url_for
from flask_dropzone import random_filename
from werkzeug.utils import secure_filename

from app.blueprint import pm_bp
from app.form.forms import PoolingForm
from app.libs import read_excel
from app.model.base import db
from app.model.project import Project


@pm_bp.route('/')
def index():
    return ''


@pm_bp.route('/import_project.html', methods=["POST", 'GET'])
def import_project():
    form = PoolingForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            f = form.pooling_file.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
            f.save(file_path)

            project_list = read_excel.read_excel(file_path)

            return redirect(url_for('views.project_table', data=project_list))
    return ''


@pm_bp.route("/upload_file", methods=["POST", 'GET'])
def upload_file():
    form = PoolingForm(request.form)
    if form.validate():
        f = form.pooling_file.data
        filename = random_filename(f.filename)

        file_path = os.path.join(current_app.config['UPLOAD_PATH'], filename)
        f.save(file_path)
        project_list = read_excel.read_excel(file_path)
        for project in project_list:

            p = Project()
            for k, v in project.items():
                p.__setattr__(k, v)
            with db.auto_commit():
                db.session.add(p)
        return "test log"

    return ''
