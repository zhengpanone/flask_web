# -*- coding: utf-8 -*-
from threading import Thread

from flask import current_app, render_template, app
from flask_mail import Message

from app import mail


# def test_send_mail():
#     msg = Message('测试邮件', sender='1216031280@qq.com', body='test', recipients=['1216031280@qq.com'])
#     mail.send(msg)

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    msg = Message('鱼书' + '' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
