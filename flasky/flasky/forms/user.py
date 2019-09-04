# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp, ValidationError

from flasky.models.user import User


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='用户名不能为空'),
                                                   Length(min=6, max=12, message='长度为6-12位'),
                                                   Regexp('^[A-Za-z0-9_.]*$', 0,
                                                          message='Username must have only letters')],
                           )
    email = StringField('email', validators=[Email(message='请输入正确的邮箱'), ],
                        )
    password = PasswordField('password',
                             validators=[DataRequired(message='密码不能为空'),
                                         Length(min=6, max=12, message="长度为6-12")],
                             )
    confirm = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                              Length(min=6, max=12, message='长度为6-12'),
                                              EqualTo('password', message='两次密码不一致')],
                            )
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError("Username already in use")


class LoginForm(FlaskForm):
    email = StringField('email', validators=[Length(2, 64), Email(message="请输入正确的密码")])
    password = PasswordField('password',
                             validators=[DataRequired(message='密码不能为空'),
                                         Length(min=6, max=12, message="长度为6-12")],
                             )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField('登陆')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Length(1, 64),
                                             Email(message="请输入正确的密码")])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), ])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), ])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Update Password')
