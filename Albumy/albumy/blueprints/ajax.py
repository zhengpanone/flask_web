# -*- coding: utf-8 -*-
from flask import render_template, jsonify
from flask_login import current_user

from albumy.blueprints import ajax_bp
from albumy.models import User, Notification


@ajax_bp.route('profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)


@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    if not current_user.is_authenticated:  # 验证登录状态
        return jsonify(message='Login required'), 403
    if not current_user.confirmed:  # 验证确认状态
        return jsonify(message='Confirm account required.'), 400
    if not current_user.can('FOLLOW'):  # 验证权限
        return jsonify(message='No permission'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(message='Already followed'), 400
    current_user.follow(user)
    return jsonify(message='User followed.')


@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    if not current_user.is_authenticated:
        return jsonify(message='Login required'), 403
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='Not follow yet.'), 400
    current_user.unfollow(user)
    return jsonify(message='Follow canceled')


@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = User.followers.count() - 1
    return jsonify(count=count)


@ajax_bp.route('/notifications-count')
def notifications_count():
    if not current_user.is_authenticated:
        return jsonify(message='Login required'), 403
    count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
    return jsonify(count=count)
