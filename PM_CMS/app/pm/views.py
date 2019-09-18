# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/9/6 9:34
"""
from app.extensions import db
from app.pm import pm


@pm.route('/insert')
def test():
    user = {'name': "Michael", 'age': 18, 'scores': [{'course': 'Math', 'score': 76}]}
    db.db.users.insert_one(user)
    return "Test Flask"
