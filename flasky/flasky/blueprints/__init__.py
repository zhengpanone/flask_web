# -*- coding: utf-8 -*-
from flasky.models.user import Permission
from flasky.blueprints.user import user
from flasky.blueprints.main import main

BluePrint = [
    (user, '/user'),
    (main, '/main')
]


def config_blueprint(app):
    for blueprint, prefix in BluePrint:
        app.register_blueprint(blueprint, url_prefix=prefix)


@main.app_context_processor
def inject_permissions():
    """
    模板中可能需要检查权限,所以将Permission类所有常量能在模板中访问
    将Permission类加入模板上下文
    :return:
    """
    return dict(Permission=Permission)
