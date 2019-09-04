# -*- coding: utf-8 -*-

from flasky import create_app

# 调用create_app函数
app = create_app('default')

if __name__ == '__main__':
    app.run()
