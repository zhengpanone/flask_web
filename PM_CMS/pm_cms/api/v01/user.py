# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/29 9:37
"""

# import lib
from flask import jsonify, g

from pm_cms.libs.enums import ClientTypeEnum
from pm_cms.libs.error_code import DeleteSuccess, AuthFailed, Success
from pm_cms.libs.redprint import RedPrint
from pm_cms.libs.token_auth import auth
from pm_cms.model.base import db
from pm_cms.model.user import User
from pm_cms.validators.user_form import ClientForm, UserEmailForm

api = RedPrint('user')


@api.route('/register', methods=['POST'])
def register_by_client_type():
    """
    根据客户端种类进行注册
    :return:
    """
    # request.args.to_dict()
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MINA: __register_user_by_mina
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)


def __register_user_by_mina():
    pass


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
