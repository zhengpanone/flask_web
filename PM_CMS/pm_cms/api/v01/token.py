# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/29 9:00
"""

# import lib
from collections import namedtuple

from flask import current_app, jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from pm_cms.libs.enums import ClientTypeEnum
from pm_cms.libs.error_code import AuthFailed, Forbidden
from pm_cms.libs.redprint import RedPrint
from pm_cms.libs.scope import is_in_scope
from pm_cms.model.user import User
from pm_cms.validators.user_form import ClientForm

api = RedPrint('token')

User_namedtuple = namedtuple('User', ['uid', 'ac_type', 'scope'])


@api.route('/', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = promise[ClientTypeEnum(form.type.data)](form.account.data,
                                                       form.secret.data)
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auto_token(identity['uid'], form.type.data, identity['scope'], expiration)
    t = {'token': token.decode('ascii')}
    return jsonify(t), 201


def generate_auto_token(uid, ac_type, scope=None, expiration=7200):
    """
    校验token
    :param uid: 用户ID
    :param ac_type: 客户端类型
    :param scope: 作用域
    :param expiration: 过期时间
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'uid': uid, 'type': ac_type.value, 'scope': scope})


def verify_auth_token(token):
    """
    解密token
    :param token:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User_namedtuple(uid, ac_type, scope)
