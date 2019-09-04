# -*- coding: utf-8 -*-
import time
import threading

from werkzeug.local import LocalStack

'''使用线程隔离的意义:使当前线程能够正确引用到他自己所创建的对象，而不是引用到其他线程所创建的对象'''

s = LocalStack()
s.push(1)
print(s.top)
print(s.top)
print(s.pop())
print(s.top)

s.push(1)
s.push(2)
print(s.top)
print(s.top)
print(s.pop())
print(s.top)

my_stack = LocalStack()
my_stack.push(1)
print('in main thread after push ,value is :' + str(my_stack.top))


def worker():
    # new thread
    print('in new thread before push ,value is :' + str(my_stack.top))
    print('in new thread after push ,value is :' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='zhengpan_thread')
new_t.start()
time.sleep(1)
# 主线程
print('finally,in main thread value is :' + str(my_stack.top))
