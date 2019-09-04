# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from flasky.extensions import db
from flasky.forms.user import LoginForm, RegisterForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm, \
    ChangePasswordForm
from flasky.lib.email import send_email
from flasky.models.user import User

user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(to=user.email, subject='Confirmation You Account', template='email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            _next = request.args.get('next')
            if _next is None or not _next.startwith('/'):
                _next = url_for('main.index')
            return redirect(_next)
        flash('Invalid username or password')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


# 更新已登陆用户的访问时间
@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'user' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email, subject='Confirmation You Account', template='email/confirm', user=user,
               token=token)
    flash('A confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))


# 退出登录
@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed you account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


# 忘记密码
@user.route("/reset", methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(to=user.email, subject='Reset Your Password', template='email/reset_password', user=user,
                       token=token)
            flash('An email with instructions to reset your password has been '
                  'sent to you.')
            return redirect(url_for('user.login'))
    return render_template("user/reset_password.html", form=form)


# 忘记密码 ，进行密码重置
@user.route("/reset/<token>", methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('user/reset_password.html', form=form)


# 修改邮箱
@user.route("/change_email_request")
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(to=new_email, subject='Confirm your email address', template='email/change_email',
                       user=current_user,
                       token=token)
            flash('An email with instructions to confirm your new email address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("user/change_email.html", form=form)


@user.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash("Invalid request.")
    return redirect(url_for('main.index'))


@user.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid password.")

    return render_template("user/change_password.html", form=form)
