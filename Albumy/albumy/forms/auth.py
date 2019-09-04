from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from albumy.models import User


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('re_password')])
    re_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in user.')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField()


class ForgetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('re_password')])
    re_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField()
