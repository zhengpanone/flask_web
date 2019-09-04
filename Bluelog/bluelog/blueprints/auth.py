# -*- coding: utf-8 -*-
from flask import url_for, redirect, flash, render_template, session
from flask_login import current_user, login_user, logout_user, login_required

from bluelog.extensions import db
from bluelog.blueprints import auth_bp
from bluelog.forms import LoginForm, RegisterForm
from bluelog.models import Admin
from bluelog.utils import redirect_back


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()

        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                session.permanent = True

                flash('Welcome back.', 'info')
                return redirect_back()  # 返回上一个页面
            flash('Invalid username or password', 'warning')
        else:
            flash('No account.', 'warning')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # TODO 用户注册视图
    form = RegisterForm()
    if form.validate_on_submit():
        admin = Admin(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
