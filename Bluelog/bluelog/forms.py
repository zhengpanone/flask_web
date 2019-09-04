# -*- coding: utf-8 -*-
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Optional, URL, StopValidation, Regexp

from bluelog.models import Category, Admin


def is_not_none(message=None):
    """自定义全局验证器"""
    if message is None:
        message = '不能为空'

        def _is_not_none(form, field):
            if not field.data:
                raise StopValidation(message)

        return _is_not_none


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 36),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or underscores')
    ])
    password = PasswordField('Password', validators=[is_not_none(), Length(6, 36)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    # TODO 用户注册
    email = StringField()
    username = StringField()
    password = PasswordField()
    password2 = PasswordField()
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register')

    def validate_username(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        """Flask_SQLAlchemy 依赖程序上下文才能正常工作，所有查询调用要放到构造方法中执行"""
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    """分类表单"""
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(3, 50)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()
