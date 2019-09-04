import os

from flask import render_template, request, current_app, send_from_directory, url_for, flash, redirect, abort
from flask_dropzone import random_filename
from flask_login import login_required, current_user
from sqlalchemy import func

from albumy.decorators import confirm_required, permission_required
from albumy.extensions import db
from albumy.blueprints import main_bp
from albumy.forms.main import DescriptionForm, TagForm
from albumy.models import Photo, Tag, Collect, Notification, Follow, User
from albumy.utils import resize_image, flash_errors, redirect_back


@main_bp.route('/')
def index():
    pass


@main_bp.route("/upload", methods=['GET', 'POST'])
@login_required  # 验证登录
@confirm_required  # 验证确认状态
@permission_required('UPLOAD')  # 验证权限
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')  # 获取图片文件对象
        filename = random_filename(f.filename)  # 生成随机文件名
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['medium'])
        photo = Photo(filename=filename,
                      filename_s=filename_s,
                      filename_m=filename_m,
                      author=current_app._get_current_object())
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)


@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    description_form = DescriptionForm()
    description_form.description.data = photo.description
    return render_template('main/photo.html', photo=photo, description_form=description_form)


@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
    """
    获取下一张
    :param photo_id:
    :return:
    """
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id) \
        .order_by(Photo.id.desc()).first()
    if photo_n is None:
        flash("This is already the last one", 'info')
        return redirect(url_for('main.show_photo', photo_id=photo_id))
    render_template(url_for('main.show_photo', photo_id=photo_n.id))


@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
    """
    获取上一张
    :param photo_id:
    :return:
    """
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id) \
        .order_by(Photo.id.asc()).first()
    if photo_p is None:
        flash('This is already the first one', 'info')
        return redirect(url_for('main.show_photo', photo_id=photo_id))
    render_template(url_for('main.show_photo', photo_id=photo_p.id))


@main_bp.route('/delete/photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can("MODERATE"):
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted', 'info')
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo.id) \
        .oreder_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id) \
            .order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('main.show_photo', photo_id=photo_p.id))
    return redirect(url_for('main.show_photo', photo_id=photo_n.id))


@main_bp.route('/report/photo/<int:photo_id>', methods=['POST'])
def report_photo(photo_id):
    """
    举报图片
    :param photo_id:
    :return:
    """
    photo = Photo.query.get_or_404(photo_id)
    photo.flag += 1  # 举报次数叠加
    db.session.commit()
    flash('Photo reported', 'success')
    return redirect(url_for('main.show_photo', photo_id=photo.id))


@main_bp.route('/photo/<int:photo_id>/description', methods=['POST'])
@login_required
def edit_description(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can("MODERATE"):
        abort(403)
    form = DescriptionForm()
    if form.validate_on_submit():
        photo.description = form.description.data
        db.session.commit()
        flash('Description update', 'success')
        flash_errors(form)
    return redirect(url_for('main.show_photo', photo_id=photo_id))


@main_bp.route('/photo/<int:photo_id>/tag/new', methods=['POST'])
@login_required
def new_tag(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can("MODERATE"):
        abort(403)
    form = TagForm()
    if form.validate_on_submit():
        for name in form.tag.data.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:  # 如果没有该标签则创建
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in photo.tags:  # 如果还没有建立联系，则建立联系
                photo.tags.append(tag)
                db.session.commit()
        flash('Tag added.', 'success')
    flash_errors(form)
    return redirect(url_for('main.show_photo', photo_id=photo_id))


@main_bp.route('/delete/tag/<int:photo_id>/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(photo_id, tag_id):
    tag = Tag.query.get_or_404(tag_id)
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can("MODERATE"):
        abort(403)
    photo.tags.remove(tag)
    db.session.commit()

    if not tag.photos:  # 如果该标签没有图片与之建立关联，就删除标签
        db.session.delete(tag)
        db.session.commit()
    flash('Tag deleted.', 'info')
    return redirect(url_for('main.show_photo', photo_id=photo_id))


@main_bp.route('/tag/<int:tag_id>', defaults={'order': 'by_time'})
@main_bp.route('/tag/<int:tag_id>/<order>')
def show_tag(tag_id, order):
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    order_rule = 'time'
    pagination = Photo.query.with_parent(tag).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items
    if order == 'by_collects':
        photos.sort(key=lambda x: len(x.collectors), reverse=True)
        order_rule = 'collects'
    return render_template('main/tag.html', tag=tag, pagination=pagination, photos=photos, order_rule=order_rule)


@main_bp.route('/collect/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required
@permission_required('COLLECT')
def collect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user.is_collection(photo):
        flash("Already collected.", 'info')
        return redirect(url_for('main.show_photo', photo_id=photo_id))
    current_user.collect(photo)
    flash('Photo collected', 'success')
    return redirect(url_for('main.show_photo', photo_id=photo_id))


@main_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
@login_required
def uncollect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if not current_user.is_collecting(photo):
        flash('Not collect yet.', 'info')
        return redirect(url_for('main.show_photo', photo_id=photo_id))
    current_user.uncollect(photo)
    flash('Photo uncollected', 'info')
    return redirect(url_for('main.show_photo', photo_id=photo_id))


@main_bp.route('/photo/<int:photo_id>/collectors')
def show_collectors(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = Collect.query.with_parent(photo).order_by(Collect.timestamp.asc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('main/collectors.html', collects=collects, photo=photo, pagination=pagination)


@main_bp.route('/notifications')
@login_required
def show_notifications():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_NOTIFICATION_PER_PAGE']
    notifications = Notification.query.with_parent(current_user)
    filter_rule = request.args.get('filter')
    if filter_rule == 'unread':
        notifications = notifications.filter_by(is_read=False)
    pagination = notifications.order_by(Notification.timestamp.desc()).paginate(page, per_page)
    notifications = pagination.items
    return render_template('main/notifications.html', pagination=pagination, notifications=notifications)


@main_bp.route('/notification/read/<int:notification_id>', methods=['POST'])
def read_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if current_user != notification.receiver:
        abort(403)
    notification.is_read = True
    db.session.commit()
    flash('Notification archived.', 'success')
    return redirect(url_for('main.show_notifications'))


@main_bp.route('/notifications/read/all', methods=['POST'])
def read_all_notification():
    for notification in current_user.notifications:
        notification.is_read = True
    db.session.commit()
    flash('All notifications archived', 'success')
    return redirect(url_for('main.show_notifications'))


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
        pagination = Photo.query.join(Follow, Follow.followed_id == current_user.id).order_by(
            Photo.timestamp.desc()).paginate(page, per_page)
        photos = pagination.items
    else:
        pagination = None
        photos = None
    tags = Tag.query.join(Tag.photos).group_by(Tag.id).order_by(func.count(Photo.id).desc()).limit(10)
    return render_template('main/index.html', pagination=pagination, photos=photos, tags=tags, Collect=Collect)


@main_bp.route("/explore")
def explore():
    # PostgreSQL和SQLite来说，随机函数为func.random（）；
    # MySQL的随机函数为func.rand（）；
    # Oracle则使用'dbms_random.value'
    photos = Photo.query.order_by(func.random()).limit(12)
    return render_template('main/explore.html', photos=photos)


@main_bp.route("/search")
def search():
    q = request.args.get('q', '')
    if q == "":
        flash('Enter keyword about photo, user or tag.', 'warning')
        return redirect_back()
    category = request.args.get('category', 'photo')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_SEARCH_RESULT_PER_PAGE']
    if category == 'user':
        pagination = User.query.whooshee_search(q).paginate(page, per_page)
    elif category == 'tag':
        pagination = Tag.query.whooshee_search(q).paginate(page, per_page)
    else:
        pagination = Photo.query.whooshee_search(q).paginate(page, per_page)
    results = pagination.items
    return render_template('main/search.html', q=q, results=results, pagination=pagination)
