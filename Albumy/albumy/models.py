# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import current_app
from flask_avatars import Identicon
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from albumy.extensions import db, whooshee


class Follow(db.Model):
    # 两侧都在同一个User模型中，这种关系被称为自引用关系（Self-Referential Many-to-Many Relationship）。
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, comment='关注者id')
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, comment='被关注者id')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')


@whooshee.register_model('username', 'name')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 资料
    username = db.Column(db.String(20), unique=True, index=True, comment="用户名")
    email = db.Column(db.String(254), unique=True, index=True, comment="邮箱")
    password_hash = db.Column(db.String(128), comment="密码")
    name = db.Column(db.String(30), comment="真实姓名")
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50), comment="城市")
    member_since = db.Column(db.DateTime, default=datetime.utcnow, comment="用户加入时间")
    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')  # back_populates是用来取代backref
    photos = db.relationship('Photo', back_populates='author', cascade='all')  # 级联关系设为all,当用户被删除时对应的图片记录也被删除

    avatar_s = db.Column(db.String(64), comment="小图")
    avatar_m = db.Column(db.String(64), comment="中图")
    avatar_l = db.Column(db.String(64), comment="大图")

    collections = db.relationship('Collect', back_populates='collector', cascade='all')

    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower',
                                lazy='dynamic', cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed',
                                lazy='dynamic', cascade='all')

    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')

    avatar_raw = db.Column(db.String(64), comment='用户上传头像文件原图文件名')

    receive_comment_notification = db.Column(db.Boolean, default=True)
    receive_follow_notification = db.Column(db.Boolean, default=True)
    receive_collect_notification = db.Column(db.Boolean, default=True)

    show_collections = db.Column(db.Boolean, default=True, comment="收藏仅自己可见")

    locked = db.Column(db.Boolean, default=False, comment="是否被锁定")

    active = db.Column(db.Boolean, default=True, comment="封禁和解禁")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()
        self.generate_avatar()
        self.follow(self)

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is None and permission in self.role.permissions

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    def collect(self, photo):
        """
        收藏图片
        :param photo:
        :return:
        """
        if not self.is_collecting(photo):
            collect = Collect(collector=self, collected=photo)
            db.session.add(collect)
            db.session.commit()

    def uncollect(self, photo):
        """
        取消收藏图片
        :param photo:
        :return:
        """
        collect = self.collected.filter_by(collected_id=photo.id).first()
        if collect:
            db.session.delete(collect)
            db.session.commit()

    def is_collecting(self, photo):
        return self.collected.filter_by(collected_id=photo.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def follow_self_all(self):
        for user in User.query.all():
            user.follow(user)

    def lock(self):
        self.locked = True
        self.role = Role.query.filter_by(name='Locked').first()
        db.session.commit()

    def unlock(self):
        self.locked = False
        self.role = Role.query.filter_by(name='User').first()
        db.session.commit()

    @property
    def is_active(self):
        return self.active

    def block(self):
        self.active = False
        db.session.commit()

    def unblock(self):
        self.active = True
        db.session.commit()


def init_role_permission():
    for user in User.query.all():
        if user.role is None:
            if user.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                user.role = Role.query.filter_by(name='Administrator').first()
            else:
                user.role = Role.query.filter_by(name='User').first()
        db.session.add(user)
    db.session.commit()


roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, comment="角色名称")
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],  # 被锁定用户
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],  # 普通用户
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],  # 协管员
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']  # 管理员
        }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
            db.session.commit()


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, comment="权限名称")
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


"""
标签和图片的多对多关系关联表
"""
tagging = db.Table('tagging',
                   db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                   )


@whooshee.register_model('description')
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), comment='图片描述')
    filename = db.Column(db.String(64), comment='文件名')
    filename_s = db.Column(db.String(64), comment="小尺寸图片文件名")
    filename_m = db.Column(db.String(64), comment="大尺寸图片文件名")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, comment='上传时间')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='photos')
    tags = db.relationship('Tag', secondary=tagging, back_populates='photos')

    collectors = db.relationship('Collect', back_populates='collected', cascade='all')


@whooshee.register_model('name')
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, comment='标签名')
    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


class Collect(db.Model):
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, comment='收藏者id')
    collected_id = db.Column(db.Integer, db.ForeignKey('photo.id'), primary_key=True, comment='被收藏图片id')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    collector = db.relationship('User', back_populates='collections', lazy='joined')
    collected = db.relationship('Photo', back_populates='collectors', lazy='joined')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False, comment='消息正文')
    is_read = db.Column(db.Boolean, default=False, comment="是否阅读")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', back_populates='notifications')


@db.event.listens_for(Photo, 'after_delete', named=True)
def delete_photo(**kwargs):
    """
    图片删除事件监听函数
    :param kwargs:
    :return:
    """
    target = kwargs['target']
    for filename in [target.filename, target.filename_s, target.filename_m]:
        if filename is not None:
            path = os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename)
            if os.path.exists(path):
                os.remove(path)


@db.event.listens_for(User, 'after_delete', named=True)
def delete_avatars(**kwargs):
    """
    删除头像文件的监听函数
    :param kwargs:
    :return:
    """
    target = kwargs['target']
    for filename in [target.avatar_s, target.avatar_m, target.avatar_l, target.avatar_raw]:
        if filename is not None:
            path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
            if os.path.exists(path):
                os.remove(path)
