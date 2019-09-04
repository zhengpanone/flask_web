# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime

from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flasky.extensions import login_manager, db
from flasky.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'users'
    name = Column(String(64), comment="真实姓名")
    username = Column(String(64), unique=True, comment="登陆名")
    _password = Column('password', String(128), comment="密码")
    email = Column(String(40), comment="邮箱")
    confirmed = Column(Boolean, default=False, comment='是否验证')
    location = Column(String(64), comment="所在地")
    about_me = Column(Text(), comment="自我介绍")
    member_since = Column(DateTime(), default=datetime.utcnow, comment="注册时间")
    last_seen = Column(DateTime(), default=datetime.utcnow, comment="最后登陆时间")
    role_id = Column(Integer, ForeignKey('roles.id'), comment="角色id")
    avatar_hash = Column(String(32), comment='缓存MD5')

    posts = relationship('Post', backref='user', lazy='dynamic')  # user和post一对多的关系

    # User 类个构造函数首先调用基类的构造函数，如果创建基类对象后还没有定义角色，则根据电子邮件地址决定将其设为管理员还是默认角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == 'zhengpanone@hotmail.com':
                # if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 密码设置为hash
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        生成用户图像
        :param size:图像尺寸,单位为像素
        :param default:
        :param rating:
        :return:
        """
        if request.is_secure:
            url = 'http://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default,
                                                                     rating=rating)

    # 校验两次密码
    def verify_password(self, password):
        return check_password_hash(self._password, password)

    # 生成令牌，有效期默认未一个小时
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    # 忘记密码，校验令牌，修改密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # 账号激活校验令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 修改密码生成token
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    # 检查用户是否有指定权限，在请求和赋予角色两种权限之间进行操作
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """经常检查是否具有管理员权限"""
        return self.can(Permission.ADMIN)

    def ping(self):
        """
        用户每次登陆都会刷新最后登陆时间
        :return:
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.name


# 出于一致性考虑，定义AnonymousUser，实现can()方法和is_administrator(),对象继承Flask-login ，将其设为用户未登录时的current_user的指
class AnonymousUser(AnonymousUserMixin):
    """AnonymousUser 实现can()和is_administrator()方法,这样无须检查用户是否登录"""

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser  # 自定义匿名用户类


# 加载用户的回调函数，接收以Unicode 字符串表示用户的标识符，如果找到用户返回用户对象，否则返回None
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(Base):
    __tablename__ = 'roles'
    name = Column(String(64), unique=True, comment="角色名称")
    default = Column(Boolean, default=True, index=True, comment='')
    permissions = Column(Integer, comment='权限')
    users = relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        """角色添加到数据库"""
        roles = {
            # 管理员
            'User': [Permission.FOLLOW, Permission.COMMENT,
                     Permission.WRITE],
            # 协管员
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            # 管理员
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Permission:
    """
    使用2的幂表示权限：每种不同的权限组合对应的值都是唯一的,方便存入角色permissions字段
    FOLLOW+COMMENT=3。通过这种方式存储各个角色的权限比较高效
    """
    FOLLOW = 1  # 关注用户
    COMMENT = 2  # 在他人文章发表评论
    WRITE = 4  # 写文章
    MODERATE = 8  # 管理他人发表的评论
    ADMIN = 16  # 管理员权限
