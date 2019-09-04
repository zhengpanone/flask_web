# -*- coding: utf-8 -*-

import threading
import time


def worker():
    print('I am thread')
    t = threading.current_thread()
    time.sleep(8)
    print('当前线程：', t.getName())


new_t = threading.Thread(target=worker, name='zhengpan_thread')
new_t.start()

t = threading.current_thread()
print('当前主线程：', t.getName())
