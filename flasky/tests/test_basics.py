# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/5/5 19:48
"""

# import lib
import unittest

from flask import current_app

from flasky import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """
        测试之前运行,尝试创建一个测试环境,尽量与正常运行应用所需环境一致
        :return:
        """
        self.app = create_app('testing')  # 使用测试配置创建应用
        self.app_context = self.app.app_context()  # 激活上下文
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        测试运行之后
        数据库和应用上下文在 tearDown() 方法中删除
        :return:
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_test(self):
        self.assertTrue(current_app.config['TESTING'])
