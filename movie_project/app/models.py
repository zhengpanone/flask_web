# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger, BigInteger
from sqlalchemy.orm import relationship
import cymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+cymysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class User(Model):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 昵称
    pwd = Column(String(100))  # 密码
    email = Column(String(100), unique=True)  # 邮箱
    phone = Column(String(11), unique=True)  # 手机
    info = Column(Text)  # 简介
    face = Column(String(255), unique=True)  # 图像
    addtime = Column(DateTime, index=True, default=datetime.now)  # 注册时间
    uid = Column(String(255), unique=True)  # 唯一标识符
    userlogs = relationship("Userlog", backref="user")  # 会员日志外键关联
    comments = relationship("Comment", backref="user")  # 评论外键关联
    moviecols = relationship("Moviecol", backref="user")  # 收藏外键关联

    def __repr__(self):
        return "<User %r>" % self.name


class Userlog(Model):
    __table__ = "userlog"
    id = Column(Integer, primary_key=True)  # 编号
    user_id = Column(Integer, ForeignKey("user.id"))  # 用户id
    ip = Column(String(100))  # 登录ip地址
    addtime = Column(DateTime, index=True, default=datetime.now)  # 登陆时间

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(Model):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, comment="编号")
    name = Column(String(100), unique=True, comment="标题")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")
    movies = relationship("Movie", backref="tag")  # 电影外键关联

    def __repr__(self):
        return "<Tag %r>" % self.name


# 上映预告
class Movie(Model):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, comment="编号")
    title = Column(String(255), unique=True, comment="标题")
    url = Column(String(255), unique=True, comment="地址")
    info = Column(Text, comment="简介")
    logo = Column(String(255), unique=True, comment="封面")
    star = Column(SmallInteger, comment="星级")
    playnum = Column(BigInteger, comment="播放量")
    commentnum = Column(BigInteger, comment="评论量")
    tag_id = Column(Integer, ForeignKey("tag.id"), comment="所属标签")
    area = Column(String(255), comment="上映地区")
    release_time = Column(DateTime, index=True, default=datetime.now, comment="上映时间")
    length = Column(String(100), comment="播放时长")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")
    comments = relationship("Comment", backref="movie")  # 电影外键关联
    moviecols = relationship("Moviecol", backref="movie")  # 收藏外键关联

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(Model):
    __tablename__ = "preview"
    id = Column(Integer, primary_key=True, comment="编号")
    title = Column(String(255), unique=True, comment="标题")
    logo = Column(String(255), unique=True, comment="封面")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(Model):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, comment="编号")
    content = Column(Text, comment="评论")
    movie_id = Column(Integer, ForeignKey("movie.id"), comment="电影编号")
    user_id = Column(Integer, ForeignKey("user.id"), comment="用户编号")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(Model):
    __tablename__ = "moviecol"
    id = Column(Integer, primary_key=True, comment="编号")
    movie_id = Column(Integer, ForeignKey("movie.id"), comment="电影编号")
    user_id = Column(Integer, ForeignKey("user.id"), comment="用户编号")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(Model):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True, comment="编号")
    name = Column(String(100), unique=True, comment="名称")
    url = Column(String(255), unique=True, comment="地址")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, comment="编号")
    name = Column(String(100), unique=True, comment="名称")
    auths = Column(String(600), unique=True, comment="权限")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")

    def __repr__(self):
        return "<Auth %r>" % self.name


# 管理员
class Admin(Model):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 昵称
    pwd = Column(String(100))  # 密码
    is_super = Column(SmallInteger, comment="是否为超级管理员")
    role_id = Column(Integer, ForeignKey("role.id"), comment="所属角色")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="添加时间")
    adminlogs = relationship("Adminlog", backref="admin")  # 管理员登陆日志外键关联
    oplogs = relationship("Oplog", backref="admin")  # 管理员操作日志外键关联

    def __repr__(self):
        return "<User %r>" % self.name


# 登陆日志
class Adminlog(Model):
    __table__ = "adminlog"
    id = Column(Integer, primary_key=True, comment="编号")
    admin_id = Column(Integer, ForeignKey("admin.id"), comment="所属管理员")
    ip = Column(String(100), comment="登录ip地址")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="登陆时间")

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 操作日志
class Oplog(Model):
    __table__ = "oplog"
    id = Column(Integer, primary_key=True, comment="编号")
    admin_id = Column(Integer, ForeignKey("admin.id"), comment="所属管理员")
    ip = Column(String(100), comment="登录ip地址")
    addtime = Column(DateTime, index=True, default=datetime.now, comment="登陆时间")
    reason = Column(String(600), comment="操作原因")

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    db.create_all()
    role = Role(name="超级管理员", auths="")
    db.session.add(role)
    db.session.commit()
