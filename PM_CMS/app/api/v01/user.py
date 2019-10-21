# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/29 9:37
"""

# import lib
from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.model.base import db
from app.model.user import User

api = RedPrint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    scope = g.user.scope
    if not scope:
        raise AuthFailed()
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.id
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/update', methods=['POST'])
def update_user():
    return 'update_user'


@api.route('<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    pass


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404('User Not Fund')
        user.delete()
    return DeleteSuccess()
