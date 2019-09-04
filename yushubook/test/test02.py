# -*- coding: utf-8 -*-

import threading
import time

'''线程隔离
LocalStack Local 字典
Local 使用字典的方式实现的线程隔离
LocalStack 封装了Local实现了线程隔离的栈结构
封装 
'''

# werkzeug local Local 字典
'''
class A:
    b = 1


my_obj = A()


def worker():
    my_obj.b = 2


new_t = threading.Thread(target=worker, name='zhengpan_thread')
new_t.start()
time.sleep(1)

print(my_obj.b)
'''
from werkzeug.local import Local


class A:
    b = 1


my_obj = Local()
my_obj.b = 1


def worker():
    my_obj.b = 2
    print('in new thread b is :' + str(my_obj.b))


new_t = threading.Thread(target=worker, name='zhengpan_thread')
new_t.start()
time.sleep(1)

print('in main thread b is ', str(my_obj.b))
