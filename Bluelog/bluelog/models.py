# -*- coding: utf-8 -*-
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    """管理员模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), comment='用户名')
    password_hash = db.Column(db.String(128), comment='密码散列值')
    blog_title = db.Column(db.String(60), comment='标题')
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)
    confirmed = db.Column(db.Boolean, default=False)

    # TODO 用户邮箱验证

    @property
    def password(self):
        raise AttributeError('password_hash is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    # TODO 用户角色
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    """文章分类"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


"""定义关系的第一步是创建外键。外键是（foreign key）用来在A表存储B表的主键值以便和B表建立联系的关系字段。
因为外键只能存储单一数据（标量），所以外键总是在“多”这一侧定义。这个字段使用db.ForeignKey类定义为外键，传入关系另一侧的表名
和主键字段名，外键字段的命名没有限制。

定义关系的第二步是使用关系函数定义关系属性。关系属性在关系的出发侧定义，即一对多关系的“一”这一侧。关系属性的名称没有限制，你可以自由修改。它相当于一个快捷查
询，不会作为字段写入数据库中。这个属性并没有使用Column类声明为列，
而是使用了db.relationship（）关系函数定义为关系属性，因为这个关系属性返回多个记录，
我们称之为集合关系属性。relationship（）函数的第一个参数为关系另一侧的模型名称，它会告诉SQLAlchemy将Category类与Post类建立关系。

当这个关系属性被调用时，SQLAlchemy会找到关系另一侧（即Post表）的外键字段（即category_id），
然后反向查询post表中所有category_id值为当前表主键值（即Category.id）的记录，返回包含这些记录的列表，
"""


class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
    """评论模型"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False, comment='评论是否通过审核')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey("comment.id"))  # 设置外键指向自身id
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    # 集合关系属性replies 中的cascade参数设为all,当父评论被删除，所有子评论也删除
    replies = db.relationship('Comment', back_populates='replied', cascade='all,delete-orphan')
    # 将remote_side参数设为id字段，
    # 把id字段定义为关系的远程侧（Remote Side）,replied_id相应的变为本地侧（Local Side）
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
