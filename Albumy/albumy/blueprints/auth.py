# -*- coding: utf-8 -*-
from flask import url_for, redirect, flash, render_template
from flask_login import current_user, login_required, login_fresh, confirm_login, login_user

from albumy.blueprints import auth_bp
from albumy.email import send_confirm_email, send_reset_password_email
from albumy.extensions import db
from albumy.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from albumy.models import User
from albumy.settings import Operations
from albumy.utils import generate_token, validate_token, redirect_back


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()  # 小写处理
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)  # 设置密码
        db.session.add(user)
        db.session.commit()

        token = generate_token(user=user, operation=Operations.CONFIRM)

        send_confirm_email(user=user, token=token)
        flash("Confirm email sent ,check your inbox.", 'info')
        return redirect(url_for('auth.login'))
    return render_template("auth/register.html", form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    确认令牌
    :param token:
    :return:
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash("Account confirmed.", 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    """
    重新发送确认邮件
    :return:
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash("New email send, check your inbox ", 'info')
    return redirect(url_for("main.index"))


@auth_bp.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash("login success", 'info')
                return redirect_back()
        else:
            flash("Your account is blocked.", "warning")
            return redirect(url_for('main.index'))
        flash("Invalid email or password.", 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash("Password reset email sent, check you inbox.", "info")
            return redirect(url_for('auth.login'))
        flash("Invalid email.", "warning")
        return redirect(url_for("auth.forget_password"))
    return render_template("auth/reset_password.html", form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticate:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=form.password.data):
            flash('Password updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token.', 'danger')
            return redirect(url_for('auth.forget-password'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)
