# -*- coding: utf-8 -*-
from functools import wraps

from flask import url_for, flash, redirect, abort
from flask_login import current_user
from markupsafe import Markup


# Flask提供的Markup类可以将文本标记为安全文本，从而避免在渲染时对Jinja2进行转义
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup('Please confirm you account first.'
                             'Not receive the email?'
                             '<a class="alert-link" href="%s">Resend Confirm Email</a>'
                             % url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_function


def permission_required(permission_name):
    """
    权限验证装饰器
    :param permission_name:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)
