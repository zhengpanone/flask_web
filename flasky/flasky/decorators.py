# -*- coding: utf-8 -*-
from functools import wraps

from flask_login import current_user
from flask import abort

from flasky.models.user import Permission

''' 检查用户权限的自定义修饰器，如果用户不具有指定权限，则返回403错误 '''


def permission_required(permission):
    """检查常规权限"""

    def decorator(f):
        @wraps(f)
        def decorated_funcion(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_funcion

    return decorator


def admin_required(f):
    """检查管理员权限"""
    return permission_required(Permission.ADMIN)(f)
