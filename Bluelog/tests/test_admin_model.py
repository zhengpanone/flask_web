# coding=utf-8
# /usr/bin/env python

'''
Author:zhengpanone
Email:zhengpanone@hotmail.com

date:2019/4/3 15:51

'''
import unittest

from bluelog.models import Admin


class AdminModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        ad = Admin(password='cat')
        self.assertTrue(ad.password_hash is not None)

    def test_no_password_getter(self):
        ad = Admin(password='cat')
        with self.assertRaises(AttributeError):
            ad.password

    def test_password_verification(self):
        ad = Admin(password='cat')
        self.assertTrue(ad.validate_password('cat'))
        self.assertFalse(ad.validate_password('dog'))

    def test_password_salts_are_random(self):
        ad = Admin(password='cat')
        ad2 = Admin(password='cat')
        self.assertTrue(ad.password_hash != ad2.password_hash)
