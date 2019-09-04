# -*- coding:utf-8 -*-
# /usr/bin/env python

"""
Author:zhengpanone
Email:zhengpanone@hotmail.com
date:2019/6/24 22:38
"""

# import lib
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def read_file():
    import os
    f = open("pi_1e8.txt", "rb")
    i = 0
    x = []
    while True:
        a = str(f.read(1024))
        i = f.tell()
        if "1" in a:
            m = a.split("1")
            print("fadsfasdfafdsf=========")
            """
            adfsfnlalksdcnvpassnf
            adfsmlkasnfadlksn
            """

        elif i == -100:
            print("afsdadsf")
        else:
            print("dfafadsf+++++++++")
            pass


def read_file2(f, l):
    x = str(f.read(1024)) + l
    if "20000101" in x:
        s = x.split("20000101")[1]
    return x[-6]


def r():
    f = open("pi_1e8.txt", "rb")
    i = 0
    x = []
    while True:

        if i == 0:
            s = f.read(1024)
            i += 1
            x = s[-6:]
        else:
            x = read_file2(f,x)






if __name__ == "__main__":
    read_file()
