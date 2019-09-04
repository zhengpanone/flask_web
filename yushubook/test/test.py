# -*- coding: utf-8 -*-
from flask import Flask, current_app, request  # 导入flask对象

# Working outside of application context.
app = Flask(__name__)  # 实例化flask核心对象
# 应用上下文 对象 Flask
# 请求上下文 对象 Request
# Flask AppContext
# Request RequestContext
# 离线应用 、单元测试
'''
ctx = app.app_context()
ctx.push()  # 入栈
a = current_app
d = current_app.config['DEBUG']
ctx.pop()  # 上下文出栈
'''
with app.app_context():  # 上下文表达式
    a = current_app
    d = current_app.config['DEBUG']

'''
实现了上下文协议的对象使用with
上下文管理器
__enter__ __exit__
上下文表达式必须要返回一个上下文管理器

文件读写
'''
'''
try:
    f = open(r'D:\t.txt')
    print(f.read())
finally:
    f.close()

with open(r'') as f:
    print(f.read())
'''


class MyResource:
    def __enter__(self):
        print('connect to resource')
        a = 1
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connection')
        return True  # True 代表异常处理 False 代表抛出异常 什么不返回代表返回None

    def query(self):
        print('query data')


with MyResource() as resource:  # as后的obj_A不是上下文管理器，是上下文管理器__enter__方法返回的值
    1 / 0
    resource.query()
